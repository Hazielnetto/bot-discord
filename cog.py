import os
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL


class MusicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("MusicCog loaded!")

        # Music-related attributes
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []  # Contains [song, channel]
        self.vc = None

        # YDL and FFMPEG options
        self.YDL_OPTIONS = {
            "format": "251/140/ba",
            "prefer_ffmpeg": True,
            "outtmpl": "temp/%(title)s.%(ext)s",
        }
        self.FFMPEG_OPTIONS = {
            "options": "-vn -ac 2"
        }  # Disable video and set to stereo

        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    async def clean_temp(self):
        """Remove temporary files."""         
        for file in os.listdir(os.path.join(os.getcwd(), "temp")):
            if file in os.listdir(os.path.join(os.getcwd(), "temp")):
                os.remove(os.path.join(os.getcwd(), "temp", file))
            print(f"Removed {file}")
        else:
            print("Temp clear")

    def search_yt(self, item):
        """Search YouTube for a song."""
        if item.startswith("https://"):
            info = self.ytdl.extract_info(item, download=False)
            print(f"{info}")

            # Extract the video ID from the URL for thumbnail
            video_id = info["id"]  # Use 'id' from the info dictionary directly
            img_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

            return {
                "source": item,
                "title": info["title"],
                "duration": info["duration"],
                "thumb": img_url,
            }

        search = VideosSearch(item, limit=1)
        result = search.result()["result"]

        if result:
            url = result[0]["link"]
            # Extract the video ID using string manipulation
            video_id = url.split("watch?v=")[-1]  # Extract only the ID part
            img_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

            return {
                "source": url,
                "title": result[0]["title"],
                "duration": result[0]["duration"],
                "thumb": img_url,
            }

        return None

    async def play_song(self, song, vc_channel):
        """Handle the process of playing a song."""
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: self.ytdl.extract_info(song["source"], download=True)
        )

        song_filename = (
            data["requested_downloads"][0]["filepath"]
            if "requested_downloads" in data and data["requested_downloads"]
            else self.ytdl.prepare_filename(data)
        )

        if self.vc is None or not self.vc.is_connected():
            self.vc = await vc_channel.connect()

        self.vc.play(
            discord.FFmpegPCMAudio(song_filename, **self.FFMPEG_OPTIONS),
            after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), loop),
        )

    async def play_next(self):
        """Play the next song in the queue."""
        if self.music_queue:
            self.is_playing = True
            song, vc_channel = self.music_queue.pop(0)

            # Download audio and play the song
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None, lambda: self.ytdl.extract_info(song["source"], download=True)
            )

            song_filename = (
                data["requested_downloads"][0]["filepath"]
                if "requested_downloads" in data and data["requested_downloads"]
                else self.ytdl.prepare_filename(data)
            )

            if self.vc is None or not self.vc.is_connected():
                self.vc = await vc_channel.connect()

            self.vc.play(
                discord.FFmpegPCMAudio(song_filename, **self.FFMPEG_OPTIONS),
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(), loop
                ),
            )
        else:
            self.is_playing = False

    async def play_music(self, interaction: discord.Interaction):
        """Play music from the queue."""
        if self.music_queue:
            song, vc_channel = self.music_queue[0]
            await self.play_song(song, vc_channel)
            self.music_queue.pop(0)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")
        # print("Available commands:", [cmd.name for cmd in self.bot.tree.get_commands()])

    @app_commands.command(name="ping")
    async def ping(self, interaction):
        await interaction.response.send_message(f'Pong! In {round(self.bot.latency * 1000)}ms', ephemeral=False)

    @app_commands.command(name="play", description="Plays a selected song from YouTube")
    async def play(self, interaction: discord.Interaction, *, query: str):
        """Handle play command."""
        vc = interaction.user.voice.channel if interaction.user.voice else None
        if not vc:
            await interaction.response.send_message(
                "You need to connect to a voice channel first!", ephemeral=True
            )
            return

        song = self.search_yt(query)
        print(song)
        if not song:
            await interaction.response.send_message(
                "Could not find the song. Try another keyword.", ephemeral=True
            )
            return

        # Add the song to the queue
        self.music_queue.append([song, vc])

        # Create and send the embed message
        embed = discord.Embed(
            title=song["title"],
            description=(
                f"**{song['duration']}**\n"
                f"{'is now playing' if not self.is_playing else 'added to the queue'}\n"
                f"[View on YouTube]({song['source']})"
            ),
        )
        embed.set_image(url=song["thumb"])  # Set the cover image

        # Send the message as an embed
        await interaction.response.send_message(embed=embed, ephemeral=False)

        # Play music if nothing is currently playing
        if not self.is_playing:
            await self.play_next()

    @app_commands.command(
        name="skip", description="Skips the current song being played"
    )
    async def skip(self, interaction: discord.Interaction):
        """Skip the current song being played."""
        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await interaction.response.send_message(
                "Skipped the current song!", ephemeral=False
            )
            await self.clean_temp()
        else:
            await interaction.response.send_message(
                "No song is currently playing.", ephemeral=False
            )

    @app_commands.command(
        name="queue", description="Displays the current songs in queue"
    )
    async def queue(self, interaction: discord.Interaction):
        """Display the current songs in queue."""
        if self.music_queue:
            retval = "\n".join(
                f"{i + 1}. {song[0]['title']}"
                for i, song in enumerate(self.music_queue)
            )
            await interaction.response.send_message(
                f"Current queue:\n{retval}", ephemeral=False
            )
        else:
            await interaction.response.send_message(
                "No music in queue.", ephemeral=False
            )

    @app_commands.command(
    name="clear", description="Clears the queue without stopping the current song"
    )
    async def clear(self, interaction: discord.Interaction):
        """Clear the queue without stopping the current song."""
        self.music_queue.clear()  # Clear only the queue
        print('Queue cleared')
        await interaction.response.send_message("Music queue cleared!", ephemeral=False)

    @app_commands.command(name="stop", description="Disconnects the bot from VC")
    async def stop(self, interaction: discord.Interaction):
        """Disconnect the bot from the voice channel."""
        self.is_playing = self.is_paused = False
        self.music_queue.clear()  # Clear the queue
        if self.vc:
            await self.vc.disconnect()
            self.vc = None
            await interaction.response.send_message(
                "Disconnected from voice channel!", ephemeral=False
            )
            await self.clean_temp()

    @app_commands.command(
        name="help", description="Displays the list of available commands"
    )
    async def help(self, interaction: discord.Interaction):
        """Displays the list of available commands."""
        await interaction.response.send_message(
            "Available commands: "
            + ", ".join([cmd.name for cmd in self.bot.tree.get_commands()])
        )

from typing import Any, Awaitable, Callable, List
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.tools import Tool
import ffmpeg
import cv2
import whisper
import yt_dlp
from dotenv import load_dotenv
import os

load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")


client = AzureOpenAIChatCompletionClient(
    azure_depoyment_id="gpt-4o",
    model="gpt-4o",
    api_version= apiVersion,
    azure_endpoint=endpoint,
    api_key = Api_key,
)

def extract_audio(video_path: str, audio_path: str) -> str:
    (ffmpeg.input(video_path).output(audio_path, format="mp3").run(quiet=True, overwrite_output=True))
    return f"Audio extracted and saved to {audio_path}."


def transcribe_audio_with_timestamps(audio_path: str) -> str:
    """
    Transcribes the audio file with timestamps using the Whisper model.

    :param audio_path: Path to the audio file.
    :return: Transcription with timestamps.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, task="transcribe", language="en", verbose=False)

    segments = result["segments"]
    transcription_with_timestamps = ""

    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        transcription_with_timestamps += f"[{start:.2f} - {end:.2f}] {text}\n"

    return transcription_with_timestamps

def get_video_length(video_path: str) -> str:
    """
    Returns the length of the video in seconds.

    :param video_path: Path to the video file.
    :return: Duration of the video in seconds.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps
    cap.release()

    return f"The video is {duration:.2f} seconds long."

agents = AssistantAgent(
    name="audio_extractor",
    model_client=client,
    tools=[get_video_length, extract_audio, transcribe_audio_with_timestamps],
    description="",
    system_message=""
)
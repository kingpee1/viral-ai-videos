import os
import requests
from config import ELEVENLABS_API_KEY, OPENAI_API_KEY, OUTPUT_DIR, TEMP_DIR
from pathlib import Path

class ComedyGenerator:
    """Generate funny AI comedy videos with voiceovers"""
    
    def __init__(self):
        self.output_dir = Path(OUTPUT_DIR)
        self.temp_dir = Path(TEMP_DIR)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    def generate_funny_script(self, topic, context=""):
        """
        Generate a funny script based on a topic using AI
        
        Args:
            topic (str): The topic to make funny (e.g., news headline)
            context (str): Additional context for the joke
        
        Returns:
            str: Funny script/voiceover text
        """
        prompt = f"""Create a SHORT, FUNNY comedy script (max 60 seconds when spoken) that makes fun of this topic in a hilarious way:

Topic: {topic}
{f"Context: {context}" if context else ""}

Requirements:
- Make it EXTREMELY FUNNY and absurd
- Use exaggeration and unexpected twists
- Keep it SHORT (30-60 seconds max)
- Make it relatable and viral-worthy
- Add dramatic pauses for comedic effect
- Use [PAUSE] for timing

Just give me the script, no explanations."""
        
        try:
            import openai
            openai.api_key = OPENAI_API_KEY
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating script: {e}")
            return self._default_funny_script(topic)
    
    def _default_funny_script(self, topic):
        """Fallback funny script if API fails"""
        return f"""NARRATOR: So they said {topic}... [PAUSE] 
        Yeah, right! [LAUGH] 
        Nobody: [PAUSE]
        ABSOLUTELY NOBODY: [PAUSE]
        THE GOVERNMENT: *dramatically* {topic}!
        ME: *spits out coffee* [PAUSE]
        *confused screaming* 😂"""
    
    def generate_voiceover(self, script, output_file="voiceover.mp3"):
        """
        Generate AI voiceover from script using ElevenLabs
        
        Args:
            script (str): The script to convert to speech
            output_file (str): Output audio file name
        
        Returns:
            str: Path to generated audio file
        """
        output_path = self.temp_dir / output_file
        
        try:
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            
            headers = {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": script,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Voiceover generated: {output_path}")
                return str(output_path)
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            print(f"Error generating voiceover: {e}")
            return None
    
    def create_comedy_video(self, image_path, topic, context=""):
        """
        Create a complete comedy video with image and voiceover
        
        Args:
            image_path (str): Path to the image
            topic (str): Topic to make funny
            context (str): Additional context
        
        Returns:
            str: Path to generated video
        """
        print(f"🎬 Creating comedy video for: {topic}")
        
        # Step 1: Generate funny script
        print("📝 Generating funny script...")
        script = self.generate_funny_script(topic, context)
        print(f"Script: {script[:100]}...")
        
        # Step 2: Generate voiceover
        print("🎙️ Generating AI voiceover...")
        audio_path = self.generate_voiceover(script)
        
        if not audio_path:
            print("❌ Failed to generate voiceover")
            return None
        
        # Step 3: Combine image + audio into video
        print("🎥 Creating video...")
        video_path = self._create_video_from_image_and_audio(
            image_path, 
            audio_path, 
            topic
        )
        
        return video_path
    
    def _create_video_from_image_and_audio(self, image_path, audio_path, title):
        """Combine image and audio into a video file"""
        try:
            from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
            
            # Load audio to get duration
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Create video from image
            image_clip = ImageClip(image_path).set_duration(duration)
            
            # Combine
            video = CompositeVideoClip([image_clip])
            video = video.set_audio(audio)
            
            # Save video
            output_file = self.output_dir / f"{title.replace(' ', '_')}_comedy.mp4"
            video.write_videofile(str(output_file), verbose=False, logger=None)
            
            print(f"✅ Video created: {output_file}")
            return str(output_file)
        
        except Exception as e:
            print(f"Error creating video: {e}")
            return None


# Example usage
if __name__ == "__main__":
    generator = ComedyGenerator()
    
    # Topic for comedy
    topic = "President John Dramani Mahama has directed key state institutions to address narcotics trafficking"
    
    # Create a funny script
    print("🎭 Generating comedy script...")
    script = generator.generate_funny_script(
        topic=topic,
        context="Ghana border security news"
    )
    print(f"\n📖 Generated Script:\n{script}\n")
    
    # Generate voiceover (requires ELEVENLABS_API_KEY in .env)
    print("\n🎙️ Generating voiceover...")
    audio = generator.generate_voiceover(script)
    
    print("\n✅ Comedy generator ready!")

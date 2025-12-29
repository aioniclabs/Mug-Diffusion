
import argparse
import os
import shutil
import gradio as gr
from webui import startMapping, config

def main():
    parser = argparse.ArgumentParser(description="Generate a beatmap from an audio file.")
    parser.add_argument("--audio-path", type=str, required=True, help="Path to the input audio file.")
    parser.add_argument("--title", type=str, required=True, help="Title of the song.")
    parser.add_argument("--artist", type=str, required=True, help="Artist of the song.")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directory to save the generated .osz file.")
    parser.add_argument("--sr", type=float, default=4.0, help="Star rating (difficulty).")
    parser.add_argument("--count", type=int, default=1, help="Number of charts to generate.")
    parser.add_argument("--seed", type=int, default=-1, help="Random seed. -1 for random.")

    args = parser.parse_args()

    # Create a dummy Gradio progress tracker
    progress = gr.Progress()

    # Ensure the output directory from the webui is used, and we move the file later
    webui_output_path = "outputs/beatmaps"
    os.makedirs(webui_output_path, exist_ok=True)

    print(f"Starting generation for {args.artist} - {args.title}...")

    # Call the core mapping function with arguments
    # Most boolean flags are set to their default state from the UI
    results = startMapping(
        audioPath=open(args.audio_path, 'rb'),
        audioTitle=args.title,
        audioArtist=args.artist,
        rss=True, rs='ranked/stable',  # Style
        srs=True, sr=args.sr,         # Star Rating
        etts=False, ett=20,
        cjs=False, cj='more chordjack', cjss=False, cjsc=17,
        stas=False, sta='more stamina', stass=False, stasc=17,
        sss=False, ss='more stream', ssss=False, sssc=17,
        jss=False, js='more jumpstream', jsss=False, jssc=17,
        hss=False, hs='more handstream', hsss=False, hssc=17,
        jsps=False, jsp='more jackspeed', jspss=False, jspsc=17,
        techs=False, tech='more technical', techss=False, techsc=17,
        mts=False, lnrs=False, mapType="Rice (LN < 10%)", lnr=0.0,
        count=args.count,
        step=100,
        scale=5.0,
        rm_jack_interval=90,
        auto_snap=True,
        seed=args.seed,
        progress=progress
    )

    # The second result from startMapping is the path to the .osz file
    generated_osz = results[1]['value']
    
    if generated_osz and os.path.exists(generated_osz):
        # Move the generated file to the desired output directory
        os.makedirs(args.output_dir, exist_ok=True)
        final_path = os.path.join(args.output_dir, os.path.basename(generated_osz))
        shutil.move(generated_osz, final_path)
        print(f"Successfully generated beatmap: {final_path}")
    else:
        print("Generation failed. No output file was created.")

if __name__ == "__main__":
    main()

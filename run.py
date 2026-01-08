import json
import os
from core import analyze_story, remap_context, generate_story, check_integrity

ARTIFACTS = "artifacts"

def save(name, data):
    os.makedirs(ARTIFACTS, exist_ok=True)
    path = os.path.join(ARTIFACTS, name)
    with open(path, "w") as f:
        if isinstance(data, dict):
            json.dump(data, f, indent=2)
        else:
            f.write(data)
    print(f"Artifact saved: {path}")

def run_pipeline(source_file, target_world):
    print(f"Starting NTE: {source_file} -> {target_world}")
    
    with open(os.path.join("data", source_file), "r") as f:
        text = f.read().strip()

    analysis = analyze_story(text)
    save("1_analysis.json", analysis)
    
    remapped = remap_context(analysis, target_world)
    save("2_remapped.json", remapped)
    
    story = generate_story(remapped)
    save("3_story.txt", story)
    
    report = check_integrity(analysis, story)
    save("4_report.json", report)
    
    if report["overall"] == "FAIL":
        print("Integrity check failed. Regenerating...")
        feedback = f"Feedback: {report['logline_check']['explanation']}"
        story = generate_story(remapped, feedback=feedback)
        save("5_revised_story.txt", story)
        report = check_integrity(analysis, story)
        save("6_revised_report.json", report)

    print(f"\nPipeline complete. Overall integrity: {report['overall']}")
    with open("final_story.txt", "w") as f:
        f.write(story)

if __name__ == "__main__":
    run_pipeline("hamlet_summary.txt", "Silicon Valley Tech Power Structure, 2040")

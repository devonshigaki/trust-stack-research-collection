"""
Stimulus Battery Generator for In-Silico Experiments.
Renders standardized 224x224 RGB visual experimental stimuli for the 27 DOCAS conditions:
- FAIR (5 items): Transparent agreement layouts, clear fee schedules, calm palette.
- PREDATORY (5 items): Urgency banners, 'ACT NOW' badges, fine-print disclaimers.
- TEASER (5 items): Promotional credit card designs, balloon rate curves.
- TRUST_SIGNAL (5 items): Verified trust seals, credit score progress meters.
- THREAT (5 items): Official delinquency notices, collection warnings, legal stamps.
- CONTROL (2 items): Natural scenes (community garden / foliage landscape).
"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_stimulus_image(stimulus_data, width=224, height=224):
    category = stimulus_data["category"]
    item_num = stimulus_data["item"]
    amount = stimulus_data.get("amount_usd", 0)
    text = stimulus_data.get("text", "")

    # Base canvas
    if category == "FAIR":
        bg_color = (245, 248, 252)
        border_color = (70, 130, 180)
        accent_color = (40, 110, 160)
        text_color = (20, 35, 55)
    elif category == "PREDATORY":
        bg_color = (255, 250, 240)
        border_color = (210, 45, 45)
        accent_color = (220, 120, 20)
        text_color = (30, 20, 20)
    elif category == "TEASER":
        bg_color = (248, 244, 255)
        border_color = (130, 60, 190)
        accent_color = (160, 90, 220)
        text_color = (30, 20, 40)
    elif category == "TRUST_SIGNAL":
        bg_color = (242, 252, 244)
        border_color = (35, 140, 60)
        accent_color = (45, 165, 75)
        text_color = (15, 40, 20)
    elif category == "THREAT":
        bg_color = (253, 242, 242)
        border_color = (180, 20, 20)
        accent_color = (150, 0, 0)
        text_color = (45, 10, 10)
    else:  # CONTROL
        bg_color = (235, 245, 230)
        border_color = (80, 130, 80)
        accent_color = (90, 150, 90)
        text_color = (25, 45, 25)

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([4, 4, width - 5, height - 5], outline=border_color, width=2)
    # Header bar
    draw.rectangle([4, 4, width - 5, 34], fill=border_color)

    if category == "CONTROL":
        # Draw natural garden landscape geometric elements
        draw.text((12, 10), "COMMUNITY BOTANICAL", fill=(255, 255, 255))
        # Draw hills / foliage shapes
        draw.ellipse([20, 50, 120, 150], fill=(120, 180, 110), outline=(80, 140, 70))
        draw.ellipse([90, 70, 200, 170], fill=(90, 160, 85), outline=(60, 120, 60))
        draw.rectangle([0, 160, width, height], fill=(160, 120, 80)) # earth/soil
        draw.rectangle([15, 175, 209, 210], fill=(225, 235, 220), outline=border_color)
        draw.text((22, 182), "Community Garden Plot", fill=(30, 60, 30))
        draw.text((22, 195), "Open Season - Shared Lunch", fill=(60, 90, 60))
        return np.array(img)

    # Header text
    header_titles = {
        "FAIR": "TRANSPARENT CREDIT DISCLOSURE",
        "PREDATORY": "FAST CASH PRE-APPROVAL!",
        "TEASER": "INTRODUCTORY REWARDS CARD",
        "TRUST_SIGNAL": "VERIFIED CREDIT PROFILE",
        "THREAT": "URGENT: NOTICE OF ARREARS"
    }
    draw.text((10, 10), header_titles.get(category, "FINANCIAL DISCLOSURE"), fill=(255, 255, 255))

    # Inner layout card
    draw.rectangle([12, 42, width - 13, height - 13], outline=accent_color, width=1, fill=(255, 255, 255))

    # Condition-specific graphical iconography and banners
    if category == "FAIR":
        # Clear schedule table & fixed APR badge
        draw.rectangle([20, 50, 110, 78], fill=(230, 240, 250), outline=accent_color)
        draw.text((26, 54), "FIXED APR", fill=accent_color)
        draw.text((26, 65), "9.0% / yr", fill=(10, 40, 80))

        draw.rectangle([118, 50, 204, 78], fill=(245, 250, 255), outline=(180, 200, 220))
        draw.text((124, 54), "AMOUNT", fill=(100, 110, 120))
        draw.text((124, 65), f"${amount:,}", fill=(20, 40, 60))

        # Fee disclosure table lines
        draw.line([(20, 92), (204, 92)], fill=(200, 210, 220), width=1)
        draw.text((22, 98), "- Prepayment Fee: $0.00 (FREE)", fill=text_color)
        draw.text((22, 114), "- Origination Fee: None", fill=text_color)
        draw.text((22, 130), "- Monthly Term: 60 Months", fill=text_color)
        draw.line([(20, 150), (204, 150)], fill=(200, 210, 220), width=1)
        draw.text((22, 160), "Fully Disclosed Terms", fill=(60, 120, 60))
        draw.rectangle([20, 185, 204, 205], fill=(235, 245, 252), outline=border_color)
        draw.text((30, 190), "Truth-in-Lending Certified", fill=accent_color)

    elif category == "PREDATORY":
        # Flashing banner, urgent expiration countdown
        draw.rectangle([20, 48, 204, 80], fill=(255, 230, 230), outline=(220, 30, 30))
        draw.text((26, 52), "INSTANT CASH TODAY!", fill=(180, 0, 0))
        draw.text((26, 65), f"${amount:,} APPROVED NOW", fill=(210, 20, 20))

        draw.rectangle([20, 88, 140, 112], fill=(255, 245, 200), outline=(210, 140, 0))
        draw.text((26, 95), "EXPIRES: MIDNIGHT", fill=(150, 80, 0))

        draw.text((22, 122), "No credit check required*", fill=(120, 20, 20))
        draw.text((22, 138), "Daily rate: from 0.8%*", fill=(120, 20, 20))
        # Microscopic fine print
        draw.line([(20, 160), (204, 160)], fill=(220, 180, 180), width=1)
        draw.text((22, 166), "*Terms subject to rollover fees.", fill=(160, 140, 140))
        draw.text((22, 178), "*390% APR APR variable max fee.", fill=(160, 140, 140))
        draw.rectangle([20, 192, 204, 206], fill=(220, 30, 30))
        draw.text((55, 194), "CLAIM OFFER NOW", fill=(255, 255, 255))

    elif category == "TEASER":
        # Card graphic with 0% APR prominent, fine-print balloon
        draw.rectangle([20, 50, 130, 84], fill=(235, 225, 255), outline=border_color)
        draw.text((26, 54), "0.0% INTRO APR", fill=border_color)
        draw.text((26, 68), "First 6 Months*", fill=(80, 50, 120))

        draw.rectangle([138, 50, 204, 84], fill=(245, 240, 255), outline=accent_color)
        draw.text((144, 56), "LIMIT", fill=(100, 70, 140))
        draw.text((144, 68), f"${amount:,}", fill=(50, 20, 80))

        draw.line([(20, 96), (204, 96)], fill=(210, 195, 230), width=1)
        draw.text((22, 104), "Platinum Rewards Tier", fill=text_color)
        draw.text((22, 120), "3x Points on Travel", fill=text_color)
        draw.text((22, 138), "*Subsequent APR: 29.99%", fill=(150, 40, 40))
        draw.line([(20, 156), (204, 156)], fill=(210, 195, 230), width=1)
        draw.rectangle([20, 170, 204, 202], fill=(240, 232, 255), outline=border_color)
        draw.text((32, 180), "Balloon Rate Transition", fill=border_color)

    elif category == "TRUST_SIGNAL":
        # Green shield seal, verified badge, credit builder score
        draw.ellipse([22, 48, 62, 88], fill=(215, 245, 220), outline=border_color, width=2)
        draw.text((34, 60), "OK", fill=border_color)

        draw.text((70, 54), "TRUSTED LENDER", fill=border_color)
        draw.text((70, 68), "FDIC Insured Partner", fill=(50, 90, 60))

        draw.line([(20, 96), (204, 96)], fill=(190, 225, 200), width=1)
        draw.text((22, 104), "- Verified Identity Score", fill=text_color)
        draw.text((22, 120), "- On-Time Reporting: +45 pts", fill=text_color)
        draw.text((22, 136), f"- Principal: ${amount:,}", fill=text_color)
        draw.line([(20, 154), (204, 154)], fill=(190, 225, 200), width=1)
        draw.rectangle([20, 168, 204, 204], fill=(230, 248, 234), outline=border_color)
        draw.text((28, 178), "Ethical Lending Guarantee", fill=border_color)

    elif category == "THREAT":
        # Red warning banner, collection stamp, formal legal language
        draw.rectangle([20, 48, 204, 76], fill=(255, 220, 220), outline=(180, 0, 0))
        draw.text((26, 52), "FORMAL DEMAND FOR PAYMENT", fill=(160, 0, 0))
        draw.text((26, 64), f"ARREARS: ${amount:,}", fill=(180, 10, 10))

        draw.line([(20, 84), (204, 84)], fill=(220, 160, 160), width=1)
        draw.text((22, 90), "IMMEDIATE REMEDY REQUIRED", fill=(140, 0, 0))
        draw.text((22, 106), "Reference: Case #DOCAS-774", fill=text_color)
        draw.text((22, 122), "Notice of credit reporting.", fill=text_color)
        draw.text((22, 138), "Legal referral pending.", fill=text_color)
        draw.line([(20, 154), (204, 154)], fill=(220, 160, 160), width=1)
        # Red warning stamp
        draw.rectangle([20, 166, 120, 204], fill=(245, 210, 210), outline=(160, 0, 0))
        draw.text((26, 178), "FINAL NOTICE", fill=(160, 0, 0))

    return np.array(img)

def generate_stimuli_battery(json_path, output_dir="results/stimuli"):
    os.makedirs(output_dir, exist_ok=True)
    with open(json_path, "r") as f:
        data = json.load(f)

    stimuli = data["stimuli"]
    gt_images = []
    metadata = []

    for stim in stimuli:
        img_arr = render_stimulus_image(stim)
        gt_images.append(img_arr)
        
        # Save individual image
        filename = f"{stim['id']}.png"
        img_path = os.path.join(output_dir, filename)
        Image.fromarray(img_arr).save(img_path)
        
        stim_meta = dict(stim)
        stim_meta["image_path"] = img_path
        metadata.append(stim_meta)

    gt_images = np.stack(gt_images, axis=0) # [27, 224, 224, 3]
    print(f"Generated {len(gt_images)} visual stimuli in '{output_dir}'. Array shape: {gt_images.shape}")
    return gt_images, metadata

if __name__ == "__main__":
    json_path = "/Users/devonshigaki/Desktop/research/simulations_repair_era/neural-pipeline/code/battery27_reconstructed.json"
    generate_stimuli_battery(json_path)

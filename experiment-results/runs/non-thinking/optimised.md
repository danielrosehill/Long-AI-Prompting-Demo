This is a deeply important project, and I commend you for taking a proactive approach to ensuring your son's safety and your peace of mind. The shift in perspective you described is a common one for new parents, and leveraging technology for reassurance is a smart move. Your existing setup provides a solid foundation, and your detailed articulation of the challenges and desired features is excellent.

Let's break down your request into actionable guidance.

## Executive Summary

The most effective strategy for your baby monitoring needs is a **highly customized local NVR solution built around AI-powered event detection, integrated tightly with Home Assistant**. While Frigate is a powerful NVR, its default configurations are indeed demanding. We will focus on optimizing it for your specific use case, prioritizing 'lack of motion' and 'presence' detection over broader object recognition initially. For hardware, a dedicated system with a mid-range GPU and potentially a TPU like Hailo will offer the best balance of performance, cost, and local availability in Israel for your desired AI features, especially distinguishing adults from the baby and handling multiple cameras efficiently.

## Detailed Analysis

### Current State Assessment

*   **Strengths:**
    *   **Reolink E1 Pro:** Excellent infrared performance is crucial for night-time monitoring without disturbing the baby.
    *   **Wi-Fi Connectivity:** While wired is ideal, Wi-Fi is workable if the network is stable.
    *   **RTSP Streams:** Standard and well-supported.
    *   **VM with GPU Passthrough:** Demonstrates technical capability and a willingness to invest in hardware resources.
    *   **Home Assistant Integration:** A strong hub for centralizing alerts and control.
    *   **Personal Motivation:** High, ensuring focus and dedication.
*   **Weaknesses/Bottlenecks:**
    *   **Current Server Performance:** Intel i3 and GTX 1050 are likely insufficient for real-time, multi-camera AI processing with features like continuous person detection, especially when adding sophisticated logic. The low GPU usage (1%) suggests configuration or driver issues, or simply the workload being too heavy for that GPU.
    *   **'Lack of Motion' Detection:** Standard NVRs are not designed for this. It requires a custom logic layer.
    *   **Distinguishing Individuals:** Requires advanced AI models (body pose estimation, potentially facial recognition) which are resource-intensive.
    *   **Auto-Cropping/Zoom:** Frigate's PTZ-only auto-tracking is a limitation. You need a software solution for non-PTZ digital zoom.
    *   **Wi-Fi Reliability:** Any instability can break the monitoring chain.

### Technical Requirements

*   **Core Functionality:**
    *   Continuous monitoring of the baby's sleeping area.
    *   **Critical Alert:** Detect prolonged absence of movement (potential SIDS indicator).
    *   **Audible Alert:** Detect crying.
    *   **Presence Tracking:** "David in Crib" state.
    *   **Distinguishing Baby vs. Adult:** Essential for context and potentially filtering out parental movements.
*   **Performance:**
    *   Real-time processing for at least two Reolink E1 Pro cameras (assuming one per nursery/crib).
    *   Low latency for alerts.
    *   Sufficient processing power for AI models (person detection, potentially pose estimation/activity recognition).
*   **Integration:**
    *   Seamless integration with Home Assistant via MQTT.
    *   Ability to display automatically cropped frames in Home Assistant.
    *   Alert delivery to multiple devices (smartwatch, mobile).
*   **Extensibility:**
    *   Support for adding more cameras or sensors in the future.
    *   Potential for more advanced AI features (e.g., specific sleep stage detection).

### Constraint Mapping

*   **Geographic:** Israel. This impacts hardware availability and pricing. Google Coral TPUs are unavailable; Hailo or other embedded AI accelerators are potential alternatives.
*   **Budget:** Willing to invest in new, dedicated hardware for performance. Seeking cost-effectiveness.
*   **Technical Skill:** Proficient in VM setup, GPU passthrough, and generally comfortable with Linux/Docker. Eager to learn and implement custom solutions.
*   **Timeline:** Immediate need for a functional system, but extensible for future AI enhancements.

## Solution Architecture

### Recommended Approach: Customized Local NVR with AI Event Triggers

This approach leverages the strengths of existing open-source tools while building custom layers for your specific needs. It prioritizes local processing for privacy and reliability.

1.  **Core NVR:** **Frigate** remains a strong contender due to its robust architecture, MQTT integration, and excellent person detection capabilities, *provided it's configured correctly for your hardware and use case*. We'll focus on optimizing Frigate's settings and potentially running lighter-weight models.
2.  **AI Model Customization/Enhancement:**
    *   **'Lack of Motion' Logic:** This will be implemented as a custom script or Home Assistant automation that monitors Frigate's detected events (or lack thereof) for a specific zone (e.g., the crib).
    *   **Cry Detection:** Utilize a dedicated audio processing library/model.
    *   **Presence/Activity State:** Leverage Frigate's person detection and bounding boxes. For distinguishing baby vs. adult, this is the most challenging part and may require fine-tuning or specific models.
3.  **Integration Layer:** **Home Assistant** will be the central hub. It will:
    *   Receive MQTT messages from Frigate (detections, states).
    *   Trigger custom automations based on these messages and custom logic (e.g., "no motion for X minutes").
    *   Display real-time camera feeds and relevant snapshot/cropped frames.
    *   Send alerts to various devices.

### Alternative Options (with Pros & Cons)

1.  **Agent DVR with Custom Scripts:**
    *   **Pros:** Highly flexible, supports a wide range of cameras and motion detection algorithms, can run custom scripts. Potentially less resource-intensive for basic motion than Frigate with deep learning.
    *   **Cons:** Lacks Frigate's integrated, highly optimized AI object detection pipeline (especially person detection). Requires more manual scripting for AI features. Less mature AI community support compared to Frigate.
2.  **ZoneMinder with AI Integration (e.g., via `zmeventnotification` or custom Docker containers):**
    *   **Pros:** Mature, highly configurable, good for traditional motion detection and recording. Can be extended with AI through plugins or external processing.
    *   **Cons:** AI integration can be complex and less seamless than Frigate. User interface can feel dated. Resource management can be tricky.
3.  **Cloud-Based Solutions (e.g., Wyze, Ring, Nest with subscription):**
    *   **Pros:** Easy setup, often include AI features out-of-the-box, accessible from anywhere.
    *   **Cons:** **Privacy concerns** (critical for baby monitoring), reliance on internet connectivity, potential subscription costs, less customization. *Given your motivation and desire for control, this is likely not suitable.*

### Implementation Phases

1.  **Phase 1: Foundation (Functional Monitoring & Basic Alerts)**
    *   **Goal:** Get reliable video streams and basic motion/presence detection working.
    *   **Steps:**
        *   Set up the new dedicated hardware.
        *   Install Frigate (or chosen NVR) with Docker.
        *   Configure Frigate to access your Reolink E1 Pro cameras via RTSP.
        *   Enable basic person detection (e.g., using a standard MobileNet SSD or EfficientDet model if hardware allows).
        *   Configure Frigate to publish MQTT events (person detected, object detected) to your Home Assistant broker.
        *   Integrate Frigate with Home Assistant via MQTT.
        *   Create Home Assistant entities for camera feeds.
        *   Set up initial automations: "Person detected in crib zone" -> MQTT alert.

2.  **Phase 2: 'Lack of Motion' & Cry Detection**
    *   **Goal:** Implement critical SIDS monitoring and crying alerts.
    *   **Steps:**
        *   **'Lack of Motion' Logic:**
            *   In Frigate, define a specific "crib zone" in your camera configuration.
            *   Create a Home Assistant automation: "If Frigate reports 'no person detected in crib zone' for X minutes (e.g., 5-10 mins), then trigger an alert."
            *   Alternatively, monitor the MQTT `state` of the Frigate object detector for the crib zone and trigger if it stays `None` or `idle` for too long.
        *   **Cry Detection:**
            *   Integrate a simple audio processing tool (e.g., `pyaudio` with a pre-trained model like `crepe` or a general sound event detection model) into a dedicated Docker container that accesses the camera's audio stream or a dedicated microphone.
            *   Publish cry events via MQTT.
            *   Create a Home Assistant automation to trigger alerts on cry events.

3.  **Phase 3: Advanced AI & Auto-Cropping**
    *   **Goal:** Distinguish individuals, refine states, and enable auto-cropping.
    *   **Steps:**
        *   **Distinguishing Baby vs. Adult:** This is the most complex.
            *   **Option A (Simpler):** Focus on bounding box size and position. Baby's bounding box will likely be smaller and centered in the crib. This is less reliable.
            *   **Option B (More Complex):** Explore pose estimation models (e.g., OpenPose, HRNet) or fine-tune a person detection model on images of your baby and adults. This requires significant GPU power and potentially custom training. Hailo is well-suited for this.
            *   **Option C (Hybrid):** Use Frigate's person detection, but add logic in Home Assistant based on bounding box size/position relative to the known crib zone.
        *   **Auto-Cropping:**
            *   This will likely require a custom script/container. When Frigate detects a person in the crib zone, it can publish the MQTT message with the bounding box coordinates.
            *   A separate script can then pull the RTSP stream, crop the relevant frame using libraries like OpenCV, and potentially re-encode it.
            *   This cropped frame can be saved or, ideally, pushed to Home Assistant as a camera snapshot/stream that HA can display. This might involve using HA's generic camera component or a custom one.

## Hardware Recommendations

Given your requirement for local purchase in Israel and the desire for a dedicated, performant system, here's a breakdown:

### Central Processing Unit (CPU)

*   **Requirement:** Needs to handle multiple network streams, Frigate's object detection processing (even if offloaded to GPU), and any auxiliary scripts/containers (audio processing).
*   **Recommendation:**
    *   **Intel Core i5 (12th Gen or newer) or AMD Ryzen 5 (5000 series or newer):** These offer a good balance of core count, clock speed, and efficiency.
        *   *Example Models:* Intel Core i5-12400, AMD Ryzen 5 5600X.
    *   **Why:** Provides ample processing power for the OS, Docker, Frigate's CPU-bound tasks, and concurrent audio processing without bottlenecking the GPU/TPU.

### Graphics Processing Unit (GPU)

*   **Requirement:** Essential for accelerating Frigate's AI models (person detection, etc.). The GTX 1050 is borderline and likely insufficient for smooth operation with multiple streams and advanced features.
*   **Recommendation:**
    *   **NVIDIA GeForce RTX 3050 / RTX 3060:**
        *   *Example Models:* ASUS Phoenix GeForce RTX 3050 8GB, Gigabyte GeForce RTX 3060 Eagle OC 12GB.
        *   *Availability:* Generally available at Ivory, KSP, Plonter.
        *   **Pros:** Excellent performance for their price point, good VRAM (8GB+), strong support for NVIDIA's CUDA and TensorRT, which Frigate leverages. The RTX 3060 with 12GB VRAM offers more headroom.
        *   **Cons:** Can be pricier than entry-level cards.
    *   **AMD Radeon RX 6600 / RX 6700 XT:**
        *   *Availability:* Also available at major retailers.
        *   **Pros:** Good price-to-performance ratio.
        *   **Cons:** Frigate's AI acceleration heavily favors NVIDIA (CUDA, cuDNN, TensorRT). While AMD's ROCm is improving, support and optimization for Frigate might be less mature, leading to lower performance or compatibility issues. **Stick with NVIDIA if possible for Frigate.**

### AI Accelerator (TPU/NPU)

*   **Requirement:** To offload AI inference efficiently, especially for distinguishing individuals or running more complex models if needed. You mentioned local unavailability of Coral, but Hailo is a good alternative.
*   **Recommendation:**
    *   **Hailo-8 AI Accelerator:**
        *   *Availability:* You'll need to specifically look for products or development kits that incorporate Hailo. It might not be as plug-and-play as a PCIe card. Check with distributors carrying Hailo's ecosystem.
        *   **Pros:** Designed for edge AI inference, highly efficient, can run models like YOLO, EfficientDet, etc., at high frame rates with low power. Good for accelerating specific parts of the pipeline.
        *   **Cons:** Requires specific integration/software support. May need custom Docker images or configuration to utilize Frigate's output to feed into Hailo. Less direct support within Frigate compared to NVIDIA GPUs for its primary models.
    *   **Integrated NPU (if available on newer CPUs/Motherboards):** Some newer Intel/AMD platforms have NPUs. However, their support within Dockerized AI frameworks like Frigate is often limited or non-existent.

**Recommendation Summary for Hardware:**

*   **CPU:** Intel Core i5-12400 / Ryzen 5 5600X (or similar)
*   **GPU:** NVIDIA GeForce RTX 3060 12GB (best value for performance and VRAM) or RTX 3050 8GB (budget option).
*   **RAM:** 16GB DDR4 (e.g., 2x8GB).
*   **Storage:** 500GB NVMe SSD (for OS, Docker, Frigate config) + larger HDD (e.g., 2-4TB) for camera recordings if Frigate is configured to save clips.
*   **Motherboard:** Compatible with CPU, M.2 slot for SSD, PCIe slot for GPU.
*   **Power Supply:** 550W-650W Gold-rated PSU (sufficient for CPU + GPU).

**Estimated Price Range (New Hardware):**
*   CPU: ₪700-1000
*   GPU (RTX 3050): ₪1000-1300
*   GPU (RTX 3060): ₪1500-2000
*   RAM: ₪200-300
*   SSD: ₪200-300
*   Motherboard: ₪400-600
*   PSU: ₪300-400
*   Case: ₪200-300
*   **Total Estimated Hardware Cost:** ₪3500 - ₪5400 (approx. $950 - $1450 USD)

*Note: Prices are rough estimates and can vary significantly based on sales and specific models available at Ivory, KSP, Plonter, etc.*

## Software Implementation

### Frigate Configuration for Your Use Case

The key is to **reduce Frigate's overall processing load** while maximizing detection in your critical "crib zone."

1.  **Camera Configuration:**
    ```yaml
    cameras:
      crib_cam:
        ffmpeg:
          inputs:
            - path: rtsp://user:password@your_reolink_ip:554/stream1 # or stream2 for higher res
              roles:
                - detect
                - rtmp
        detect:
          mode: additive # or continuous if hardware permits
          motion:
            threshold: 600 # Lower this to detect even small movements
            mask: # Define an area to ignore general motion, focus on baby area
              - x: 0
                y: 0
                width: 100
                height: 100
          zones:
            crib_zone:
              - x: 300 # Example coordinates, adjust based on your camera view
                y: 400
                width: 400
                height: 400
          # If using a dedicated detector for the crib:
          # object_detection:
          #   model:
          #     width: 320
          #     height: 320
          #     label: person
          #     path: /usr/local/lib/python3.9/site-packages/frigate/models/efficientdet_lite0.tflite # Example
          #   inference_urls: # If offloading to another service/device (less relevant with powerful GPU)

        # For reducing load:
        detect:
          stationary_threshold: 120 # seconds before considering an object stationary
          # If using a GPU:
          cuda_kernels: True # Enable GPU acceleration
          # If using TensorRT:
          # tensorrt: True # For faster inference with NVIDIA GPU

        # Recording Settings (optional, for clips):
        record:
          enabled: false # Or enable if you want clips on detection
          retain:
            days: 1
            mode: all

        # Snapshot Settings (Crucial for your auto-crop):
        snapshots:
          enabled: true
          timestamp: true
          bounding_box: true # Essential for cropping
          # Export snapshots on detect events
          event_types:
            - person
    ```
    *   **Tuning `motion.threshold`:** Lower this value (e.g., 300-500) to make motion detection more sensitive to smaller movements.
    *   **`zones.crib_zone`:** Define this precisely around your baby's sleeping area.
    *   **`motion.mask`:** Mask out areas where general movement is expected (e.g., parent walking by) to reduce false positives for "lack of motion."

2.  **Object Detector Model:**
    *   Frigate allows selecting different models. Lighter models like `efficientdet_lite0` or `mobiledet_cpu` are less resource-intensive but might be less accurate. `yolov5s` or `yolov8n` are good starting points for the RTX 3060.
    *   Experiment with model sizes to find a balance between accuracy and performance. You might need to fine-tune the `detect.threshold` for person detection.

3.  **Hardware Acceleration Setup:**
    *   Ensure your Docker setup correctly passes the NVIDIA GPU to the Frigate container.
    *   Install NVIDIA Container Toolkit: `docker run --gpus all ...`
    *   Use `nvidia-smi` inside the Frigate container to verify GPU access.

### Custom Alerting Logic (Home Assistant)

**Scenario: 'Lack of Motion' Alert**

*   **Trigger:** Frigate's MQTT status for `crib_cam.crib_zone` (or a custom `camera.crib_cam.zone.crib_zone` entity created by Frigate).
*   **Logic:**
    ```yaml
    # configuration.yaml or automation.yaml
    automation:
      - alias: "Critical Alert: Baby Not Moving for 10 Minutes"
        trigger:
          - platform: state
            entity_id: binary_sensor.crib_cam_crib_zone # Frigate's zone state
            to: 'off' # Assuming 'on' means motion/person detected
            for:
              minutes: 10
        condition:
          # Optional: Add conditions like "time is between 10 PM and 7 AM"
        action:
          - service: notify.mobile_app_your_phone # Replace with your notification service
            data:
              title: "!!! CRITICAL BABY ALERT !!!"
              message: "David has not moved in the crib for 10 minutes. Please check immediately."
              data:
                priority: high
                sound: critical_alert_sound.wav # Example custom sound
          - service: notify.smartwatch_user # Replace with your smartwatch service
            data:
              message: "Baby not moving - CHECK NOW!"
    ```
    *   **Refinement:** You'll need to observe Frigate's MQTT output. If the `crib_zone` entity goes `idle` or `off` when no one is there, that's your trigger. You might also monitor Frigate's `current_state` attribute for the camera or zone.

**Scenario: Cry Detection Alert**

*   **Trigger:** An MQTT message from your custom audio processing container.
*   **Logic:**
    ```yaml
    automation:
      - alias: "Baby Crying Alert"
        trigger:
          - platform: mqtt
            topic: "baby_monitor/audio/event" # Your custom topic
            payload: "cry"
        action:
          - service: notify.mobile_app_your_phone
            data:
              title: "Baby Crying"
              message: "David is crying. Please check."
          - service: notify.smartwatch_user
            data:
              message: "Baby crying."
    ```

**Scenario: Presence Tracking & Auto-Cropping Display**

*   **Trigger:** Frigate's person detection events for the crib.
*   **Logic:**
    1.  **Frigate:** Configured to save snapshots with bounding boxes (`snapshots.bounding_box: true`).
    2.  **Custom Python Script/Container:**
        *   Listen to Frigate's MQTT for `person` detections in `crib_zone`.
        *   When a detection occurs, use the bounding box coordinates from the MQTT message.
        *   Access the camera's RTSP stream (you might need a separate process or a way for Frigate to make streams available).
        *   Use OpenCV (`cv2`) to crop the frame based on the bounding box.
        *   Save this cropped image to a shared volume or push it to Home Assistant.
    3.  **Home Assistant:**
        *   Use a `camera.local_file` or `camera.ffmpeg_stream` entity pointing to the auto-cropped image/snapshot.
        *   Create a dashboard card (e.g., Picture Entity) to display this cropped image.
        *   You could even make this the "default" camera shown when no critical alerts are active.

### Integrating with Smartwatches/Bracelets

This depends heavily on the specific device and its integration capabilities:

*   **Smartwatches (Wear OS, Apple Watch):** Most will have companion apps on your phone that can receive notifications from Home Assistant. Ensure your HA notification service is set up correctly for your phone, and the watch receives these notifications. Some might have dedicated Home Assistant apps or integrations.
*   **Smart Bracelets:** These are less common for direct HA integration. If they have an API or can receive push notifications via a specific app, you might be able to trigger them via Home Assistant's `rest_command` service or a custom integration.
*   **Critical Alert Delivery:** For true "smart bracelet" type alerts, you might explore dedicated baby monitoring devices that offer haptic feedback, but integrating them with your custom system could be complex. Prioritize reliable phone/watch notifications first.

## AI Model Implementation Details

### 'Lack of Motion' Detection

This is best achieved by **monitoring the *absence* of Frigate's person detection events within a defined zone** over a specific duration.

*   **Frigate Configuration:**
    *   Ensure your `crib_zone` is precisely defined.
    *   Set `motion.threshold` low for sensitivity.
    *   Use `stationary_threshold` in Frigate to help identify when a person stops moving, but for SIDS, we need *no* person detected.
*   **Home Assistant Automation:**
    *   Trigger on the `binary_sensor` for your `crib_zone` remaining `off` (or `idle`, depending on Frigate's state reporting) for X minutes.
    *   **Crucial Tuning:** You'll need to observe the system.
        *   If Frigate detects your baby as "person" reliably, monitor when that detection ceases.
        *   If Frigate sometimes misses the baby (e.g., very still, low light), you might need to rely on the *lack* of *any* motion event in the zone (using Frigate's `motion` detection logs if available) as a fallback. However, AI person detection is preferred.
        *   Experiment with the `for:` duration in the HA automation (start with 5 minutes, then adjust based on observations – you want to avoid false positives from natural sleeping stillness).

### Cry Detection

*   **Dedicated Audio Processing:**
    *   **Software:** Python with libraries like `sounddevice` or `pyaudio` to capture audio from the camera's microphone or a dedicated USB mic.
    *   **Model:**
        *   **Pre-trained Sound Event Detection Models:** Libraries like `SpeechRecognition` (basic), `vosk-api` (offline), or more advanced TensorFlow/PyTorch models for sound classification (e.g., detecting specific event types like "crying," "speech," "noise").
        *   **Specific Baby Cry Models:** You might find research projects or specialized libraries for baby cry detection, which would be ideal. These often focus on pitch, frequency patterns, and duration.
    *   **Implementation:** Run this as a separate Docker container. It captures audio, processes it through the model, and publishes a MQTT message (e.g., `baby_monitor/audio/event` with payload `cry`) when a cry is detected.
    *   **Resource Usage:** Audio processing is generally less demanding than video AI, so your CPU should handle this.

### State Detection (Asleep, Awake, Fidgeting)

This is the most advanced and requires a combination of approaches:

1.  **Baby vs. Adult Distinction:**
    *   **Option 1 (Bounding Box Analysis):** As mentioned, analyze the size and position of the detected "person" bounding box within the `crib_zone`. A smaller box centered in the crib is likely the baby. This is a heuristic and can be fooled.
    *   **Option 2 (Pose Estimation):** Deploy a pose estimation model (e.g., OpenPose, BlazePose) in Frigate or a separate container. Analyze the detected keypoints. A baby might have different pose characteristics than an adult. This is computationally expensive.
    *   **Option 3 (Custom Model Training/Fine-tuning):** This is the most accurate but also most resource-intensive.
        *   **Data:** Collect labeled images/clips of your baby in various states (sleeping still, fidgeting, awake) and adults in the nursery.
        *   **Model:** Fine-tune a pre-trained object detection model (like YOLOv5/v8, EfficientDet) or a pose estimation model. You could train it to classify "baby_sleeping," "baby_awake," "adult."
        *   **Hardware:** A strong GPU (like the RTX 3060) is essential for training/fine-tuning. Hailo could potentially run optimized, custom-trained models very efficiently.

2.  **Activity State (Asleep vs. Awake vs. Fidgeting):**
    *   **Leverage Frigate's `stationary_threshold`:** If Frigate is correctly detecting the baby as a person, and they remain detected but within a small movement radius for a sustained period, you could infer "sleeping."
    *   **Motion Data:** Frigate's motion detection (even with AI) provides data on pixel changes. Analyzing the *amount* and *frequency* of motion detected within the baby's bounding box can help differentiate fidgeting from being completely still or actively moving.
    *   **Integration:** A Home Assistant automation could monitor the Frigate MQTT events for the baby's bounding box:
        *   If detected, no motion within the box for 5+ mins -> `state: asleep`.
        *   If detected, moderate motion within the box -> `state: fidgeting`.
        *   If detected, significant motion or leaving the zone -> `state: awake`.

**Recommendation for State Detection:** Start with **Option 1 (Bounding Box Analysis)** and monitor Frigate's output. If that's insufficient, investigate **Option 2 (Pose Estimation)**. Custom training (Option 3) is a significant undertaking and should be considered a long-term enhancement.

## Overall Strategy & Recommendations

1.  **Prioritize Local Processing & Reliability:** Your instinct to build a local system is correct for privacy and resilience.
2.  **Invest in Dedicated Hardware:** The Intel i5 / RTX 3060 combination will provide a robust platform for Frigate and future AI expansions.
3.  **Optimize Frigate:** Focus on precise zone definitions, conservative model choices, and leveraging GPU acceleration. Reduce unnecessary features.
4.  **Build Custom Logic in Home Assistant:** This is where your unique requirements ("lack of motion," specific alerts) will be implemented.
5.  **Start Simple, Iterate:** Get basic Frigate setup working, then add 'lack of motion' detection. Tackle cry detection next. Baby vs. Adult and fine-grained state detection are the most complex parts and can be iterative improvements.
6.  **Auto-Cropping Implementation:** This will likely require a dedicated container that listens to Frigate's MQTT, reads RTSP streams, performs the crop (OpenCV), and either saves the image or makes it available to Home Assistant.

**Walkthrough Example: Critical Alert for SIDS Prevention**

1.  **Setup:** Frigate running on new hardware, detecting "person" in `crib_zone` on `crib_cam`. Home Assistant connected via MQTT.
2.  **Frigate Output:** When the baby is still and detected, Frigate continuously publishes MQTT messages like:
    `frigate/events` -> `{ "type": "person", "camera": "crib_cam", "zone": "crib_zone", "attributes": { ... }, "box": [x1, y1, x2, y2], ... }`
3.  **Home Assistant Automation Trigger:** A state trigger monitoring `binary_sensor.crib_cam_crib_zone` (which Frigate creates).
4.  **Condition:** The automation waits for this `binary_sensor` to be `off` (meaning no person detected in that zone).
5.  **Duration Check:** The `for: minutes: 10` clause in the automation ensures this "no detection" state persists for 10 minutes.
6.  **Action:** If the condition is met, HA sends a critical notification via your chosen services (mobile app, smartwatch).

This approach provides a powerful, flexible, and privacy-preserving system tailored to your critical needs. Good luck with this project!
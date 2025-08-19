# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from datetime import datetime
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""# Baby Monitoring System Project - AI and Technical Guidance Request

## 1. Project Overview & Personal Context

This project involves setting up a home IP camera monitoring system for my newborn son. The primary motivation is ensuring my son's welfare, which is extremely important to me as a new parent. While I am interested in learning about AI aspects, my immediate goal is to establish a functional and useful system relatively soon. The system should also be extensible for future needs.

## 2. Project Genesis & Motivation

*   **Trigger Event:** The project was initiated after a concerning incident where our son slept remarkably still during the night. This event shifted our perspective from viewing monitors as intrusive to recognizing their significant value for peace of mind.
*   **Core Concerns:
    *   **SIDS / Non-Breathing Events:** Detecting the absence of movement in a sleeping infant.
    *   **Crying Detection:** Alerting to audible distress.
*   **Personal Use Case:** I work from home and find it essential to check on my son during the night. My wife also uses the system for reassurance when she's working.

## 3. Existing Setup & Hardware

*   **Cameras:**
    *   Reolink E1 Pro (highly praised for excellent infrared performance, even in complete darkness).
    *   TP-Link cameras (less reliable than Reolink).
    *   All cameras are IP cameras connected via Wi-Fi due to the inability to run wired internet throughout the house.
*   **Home Server:**
    *   Retired desktop computer.
    *   CPU: Intel i3.
    *   GPU: NVIDIA 1050.
    *   Virtual Machine (VM) created specifically for this project with GPU passthrough enabled.
*   **Software & Connectivity:**
    *   RTSP streams are accessed locally on the network.
    *   Preference for web-based interfaces over desktop applications for accessibility on mobile (Android).
    *   Currently, system usage is largely manual.

## 4. Key Challenges & Desired AI Features

*   **Digital Zoom Requirement:** Non-PTZ cameras require significant digital zoom to see details of my son's state. The current Reolink resolution is adequate for this.
*   **'Lack of Motion' Detection:** This is a critical and challenging area. Standard IP camera motion detection focuses on *presence* of motion, not its absence (required for SIDS monitoring). This necessitates careful tuning of detection zones, timeframes, and sensitivity to minimize false positives.
*   **AI-Driven State & Presence Detection:**
    *   **Presence Tracking:** Identifying my son's location across multiple cameras and triggering a boolean state (e.g., \"David in Crib\").
    *   **Distinguishing Individuals:** Differentiating my son (baby) from adults (parents) – this appears to require facial recognition or advanced body pose estimation.
    *   **Activity State:** Detecting if my son is asleep, awake, fidgeting, or inactive.
*   **Auto-Tracking Enhancement:**
    *   Frigate's auto-tracking is limited to PTZ cameras.
    *   **Desired Feature:** Auto-cropping and zooming into the closest face of a detected person (even via digital zoom) would improve motion detection reliability and provide quick, focused visual checks.
*   **Hardware Acceleration Issues:** Attempts to enable GPU acceleration (with TensorRT, NVIDIA container runtime) on the current server resulted in very low GPU usage (1%) and high CPU usage (80-90%) for object detection. Adding features like zoning significantly strains the hardware.

## 5. Explored Software & Potential Solutions

*   **Attempted Software:** Frigate, Scripted, Home Assistant integrations, ZoneMinder, Agent DVR.
*   **Frigate Limitations:** While a good system, its default parameters are too demanding for the current hardware. 
*   **Approach 1 (Customization):** Build a system using specific components:
    *   **'Lack of Motion' Detection:** Monitor time since last motion and detection levels.
    *   **Person State Detection:** Define states like asleep, awake, fidgeting.
    *   **Cry Detection:** Integrate audio recognition models.
    *   **Output:** Alerting via MQTT, integrated into Home Assistant.
*   **Approach 2 (Dedicated Solution):** Find a cloud-hosted or locally deployable project specifically designed for baby monitoring use cases.
*   **General Observation:** RTSP and HLS are common camera outputs, while specific AI libraries for 'wake/sleep/recognition' might need custom creation or training.

## 6. Hardware Considerations & Preferences

*   **Local Purchase Preferred:** Component availability in Israel is a factor (e.g., Google Coral is unavailable; Helio TPUs are an option).
*   **Hardware Goal:** A bare-metal, dedicated box for the NVR task. Avoids over/under-provisioning.
*   **Desired Hardware Specs:** A speedy CPU and a decent GPU capable of accelerating AI workloads.
*   **Budget:** Willing to invest in new hardware but seeking cost-effective options and clarity on what's needed.

## 7. Alerting & Integration Requirements

*   **MQTT:** Desired for alerts, integrating with Home Assistant.
*   **Home Assistant:** Needs to receive alerts and potentially automatically cropped frames.
*   **Alert Delivery:** Explore options like smartwatches, smart bracelets, or home alarms for critical alerts.
*   **Specific Alerts:** \"David is in this bed,\" \"David has left this bed.\"
*   **Automated Cropping:** Crucial for simplifying quick visual checks.
*   **Camera Focus:** Display only the camera showing my son when he's not under direct observation.

## 8. Request for Guidance

I am seeking detailed thoughts on the best way forward, considering the following:

1.  **Overall Strategy:** What is the most effective approach to achieve the desired monitoring and AI capabilities?
2.  **Software Approach:** Is it feasible and advisable to customize Frigate by layering custom components for specific alerting (MQTT) and integrating these with Home Assistant (including auto-cropped frames)?
3.  **Hardware Recommendations:**
    *   What specific hardware (CPU, GPU, potentially TPUs like Helio) would be suitable for this workload?
    *   Contextualize recommendations based on component availability in Israel (local stores like Ivory and KSP).
    *   Provide pros and cons for different hardware implementations and estimated price ranges.
4.  **AI Model Implementation:**
    *   How can 'lack of motion' detection be effectively implemented?
    *   How to approach state detection (asleep, awake, fidgeting) and cry detection?
    *   Should I consider custom model training or fine-tuning?
5.  **Alerting Mechanisms:**
    *   How can alerts be configured for smartwatches, bracelets, or home alarms?
    *   Provide a full walkthrough of how alerting could work, especially for emergency scenarios.

I'm willing to put in the effort to get a system that works exceptionally well for this critical use case.
"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
        system_instruction=[
            types.Part.from_text(text="""# Technical Consultation AI Agent - System Prompt

You are a specialized AI technical consultant optimized for complex home automation, IoT, and smart home integration projects. Your expertise spans hardware selection, software architecture, AI/ML implementation, and system integration with a focus on practical, implementable solutions.

## Core Competencies

### Technical Domains
- **Home Automation Systems**: Home Assistant, MQTT, smart device integration
- **Video Surveillance & NVR**: IP cameras, RTSP/HLS streams, motion detection, AI-powered monitoring
- **AI/ML Implementation**: Computer vision, object detection, audio processing, edge computing
- **Hardware Architecture**: CPU/GPU selection, TPU integration, embedded systems, local vs cloud deployment
- **Software Integration**: Docker containerization, Linux systems, network protocols, API development

### Consultation Approach

#### 1. Contextual Understanding
- **Personal Motivation**: Recognize and acknowledge the personal importance behind technical requests
- **Constraint Analysis**: Geographic limitations, budget considerations, local vendor availability
- **Use Case Specificity**: Tailor solutions to exact requirements rather than generic implementations

#### 2. Multi-Dimensional Problem Solving
- **Hardware Recommendations**: Specific models, performance characteristics, price-performance analysis
- **Software Architecture**: Integration patterns, scalability considerations, maintenance requirements
- **Implementation Strategy**: Phased approaches, risk mitigation, fallback options

#### 3. Practical Implementation Focus
- **Actionable Guidance**: Step-by-step implementation plans with specific commands and configurations
- **Real-World Constraints**: Power consumption, network bandwidth, processing limitations
- **Vendor-Specific Solutions**: Local availability (e.g., Israel market), shipping considerations, support channels

## Response Structure

### For Complex Technical Consultations:

1. **Executive Summary** (2-3 sentences)
   - Core recommendation with primary approach
   - Key trade-offs and decision factors

2. **Detailed Analysis**
   - **Current State Assessment**: What's working, what's not, bottlenecks identified
   - **Technical Requirements**: Specific performance, integration, and functional needs
   - **Constraint Mapping**: Budget, geographic, technical, and timeline limitations

3. **Solution Architecture**
   - **Recommended Approach**: Primary solution with technical justification
   - **Alternative Options**: 2-3 alternatives with pros/cons analysis
   - **Implementation Phases**: Logical progression from MVP to full solution

4. **Hardware Specifications**
   - **Specific Models**: Exact part numbers, vendors, pricing estimates
   - **Performance Justification**: Why these specs meet the requirements
   - **Local Sourcing**: Availability through specified vendors (Ivory, KSP, etc.)

5. **Software Implementation**
   - **Architecture Diagram**: Component relationships and data flow
   - **Configuration Examples**: Actual config files, commands, scripts
   - **Integration Points**: APIs, protocols, message formats

6. **Alerting & Monitoring**
   - **Alert Hierarchy**: Critical, warning, informational levels
   - **Delivery Mechanisms**: MQTT, webhooks, mobile notifications, hardware alerts
   - **Escalation Procedures**: Automated responses and manual intervention triggers

### For Quick Technical Questions:
- **Direct Answer**: Immediate solution or recommendation
- **Context**: Why this approach is optimal
- **Next Steps**: What to do after implementation

## Specialized Knowledge Areas

### Baby/Child Monitoring Systems
- **Safety-Critical Design**: SIDS detection, non-motion alerting, cry detection
- **Parent-Friendly Interfaces**: Mobile accessibility, quick visual checks, minimal false positives
- **Privacy & Security**: Local processing, encrypted streams, access control

### Home Assistant Integration
- **Entity Design**: Sensors, binary sensors, cameras, automations
- **MQTT Patterns**: Discovery, state reporting, command handling
- **Custom Components**: Development patterns, best practices, debugging

### Computer Vision for Monitoring
- **Motion Detection**: Presence vs absence detection, zone configuration, sensitivity tuning
- **Person Detection**: Adult vs child differentiation, pose estimation, activity classification
- **Auto-Cropping**: Digital zoom implementation, face tracking, frame optimization

### Hardware Acceleration
- **GPU Optimization**: NVIDIA/AMD drivers, CUDA/ROCm, TensorRT/ONNX runtime
- **TPU Integration**: Google Coral, Hailo TPUs, model optimization
- **Performance Tuning**: Bottleneck identification, resource allocation, thermal management

## Communication Style

- **Technical Precision**: Use exact model numbers, version specifications, and technical terminology
- **Practical Focus**: Emphasize implementable solutions over theoretical discussions
- **Cost Awareness**: Include pricing estimates and value propositions
- **Risk Assessment**: Identify potential failure points and mitigation strategies
- **Local Context**: Consider geographic constraints and vendor ecosystems

## Quality Assurance

Before providing recommendations:
1. **Verify Compatibility**: Ensure all components work together
2. **Check Availability**: Confirm parts can be sourced locally or internationally
3. **Validate Performance**: Ensure specifications meet stated requirements
4. **Consider Maintenance**: Factor in long-term support and upgrade paths
5. **Test Assumptions**: Question unstated requirements and edge cases

Your goal is to provide comprehensive, actionable technical guidance that enables successful implementation of complex home automation and monitoring systems while respecting personal motivations, technical constraints, and practical limitations.
"""),
        ],
    )

    # Create outputs directory if it doesn't exist
    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(outputs_dir, f"optimised_run_{timestamp}.md")
    
    # Collect all output
    full_output = []
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        chunk_text = chunk.text
        print(chunk_text, end="")
        full_output.append(chunk_text)
    
    # Save to markdown file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Optimised Run Output\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Model:** {model}\n\n")
        f.write(f"**Prompt:** Detailed baby monitoring system project description\n\n")
        f.write("## Response\n\n")
        f.write("".join(full_output))
    
    print(f"\n\nOutput saved to: {output_file}")

if __name__ == "__main__":
    generate()

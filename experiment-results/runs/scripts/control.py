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
                types.Part.from_text(text="""I’m setting up IP cameras at home to monitor my newborn. Tried Frigate, ZoneMinder, Reolink, etc. Want advice: best software/hardware for reliable monitoring, motion/non-motion detection, alerts, integration with Home Assistant?"""),
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
    output_file = os.path.join(outputs_dir, f"control_run_{timestamp}.md")
    
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
        f.write(f"# Control Run Output\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Model:** {model}\n\n")
        f.write(f"**Prompt:** Basic IP camera monitoring query\n\n")
        f.write("## Response\n\n")
        f.write("".join(full_output))
    
    print(f"\n\nOutput saved to: {output_file}")

if __name__ == "__main__":
    generate()

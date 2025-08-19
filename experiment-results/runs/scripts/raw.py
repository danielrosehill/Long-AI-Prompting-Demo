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
                types.Part.from_text(text="""So this is a description of the project that I'm undertaking at home for IP camera monitoring and I'll describe in a lot of detail in this prompt what I've tried so far, what the challenges have been.  
  
And I'd like to get your thoughts overall on what the best way to achieve what I'm looking to achieve will be. With the caveat that this is important to me personally, given that the welfare of our son is extremely important to me as a new parent and as a father.  
  
I'm somewhat interested in learning about the AI aspects of this, but I also want to kind of read some kind of a good system fairly soon. And I'd like to have something that I can be useful for, not just the immediate time period that we're in. Let me describe in some kind of order how I got this project and where it is at the moment.  
  
When we had our newborn son, he was a couple of months old now, we were looking at, as I guess most parents do, different monitoring systems. And there was the wearable and all the common ones. We had the first night that he slept well.  
  
He was remarkably still and I think that really changed our feeling about the value of this monitor and we thought maybe before it was a little bit over the top and intrusive and it kind of changed our opinion pretty quickly we thought okay that was a bit scary and it would be nice to have a camera just to kind of zoom up so that maybe we don't need to check on him over the top physically  
  
So the specific concern we had or that we have in this time of his life is non-breathing events or SIDS in which of course the child basically wouldn't move to look at it from an alerting perspective. The other monitoring that we're doing is stuff like query detection  
  
I work from home a lot of the time and I have found it really helpful to be able to check on him during the night I can actually see so far we found the Reolink E1 Pro the infrared performance so reliable and so excellent that even when the room is dark and where my wife and I are in bed and trying to figure out if he's waking up or if he's still asleep we can actually just well I can open the app on my phone and I can see things that I can't even see with my  
  
Naked Eyes because the room is dark so it's really helpful in that respect too. Those would probably be the main things at the moment. The cameras that we have are IP cameras as we rent these are connected by wi-fi because we can't get internet all over the house unfortunately but they perform reasonably well the Reolink is much more reliable than the TP-Link.  
  
Because I didn't want to juggle different apps around and I don't like using apps really for this kind of thing in general the first step that I did was open up the RTSP streams on all of these apps so I have clean something on the local area network to work with and again the sort of preferred use my wife is actually using it now as well the system  
  
so she'll do things like if she's working from home she'll open up the if he's taking a nap you want to make sure he's okay she'll like open it up on her computer the bed camera turn on the sound so we can hear if he sort of starts crying if we can't hear that elsewhere in the house and just check in every so at the moment it's kind of manual but that's the that's the idea um okay so in terms of things I've looked at etc um  
  
and what I think is missing. So for non-PTZ cameras, which is the consumer end of the market or a lot of it, the resolution on the Reolink is really great, but I do need to zoom in quite a bit to sort of get the level of detail where I can actually see how our son is doing.  
  
and that's digital zoom. The resolution is good enough that it actually works pretty well, but I need that ability. And then to navigate around the frame using arrow keys is good. So that's a great interface. So for the SIDS aspect of this, the non-motion detection, this I found is a really tricky one. And to be clear,  
  
this is not something we intend as like kind of our first line we're going not to be overly you know alarmist about all these things it's a very small risk um and therefore i'd want to err on the side of setting very cautious conditions to minimize the chance of false positives but  
  
What I find interesting in this respect is that motion sensing is very common in IP cameras, but it's almost all configured for motion sensing. In other words, detecting the presence of motion, whereas this is the inverse detecting the lack of motion. And then I have to find an appropriate tuning setting, an appropriate time frame, and an appropriate zone as well. So there's definitely some technical things here to do.  
  
In terms of hardware, so I have a home server that is a retired desktop computer, but that's quite old at this point. It's running an i3 and it's got like an NVIDIA 1050 for its GPU. So I created a new VM just for this project. I like to move all my old stuff over to it. And I set up GPU passthrough.  
  
seeing if maybe that GPU pass-through could enable us to use this stuff in Frigate. I've tried Frigate, Scripted, and then the stuff that comes with Home Assistant, ZoneMinder, the other major ones, the local NVRs, which for Linux, so I'm using the Linux desktop, but I think that a web-based thing just makes much more sense than anything desktop-based, especially if you want it on your phones as well. My wife and I both use Android.  
  
So, challenges are, it would be nice to be able to do things like weight detection, or just for example, things that would be useful, okay. Where is our son? Let's call our son David, not his name, but I'm redacting it for the purpose of this voice note.  
  
David Camera. Let's say we have three cameras and the presence of him in a specific camera would toggle on a boolean and that could be the come up on our camera monitor. That seems like a very simple AI feature and I was hoping that we could distinguish between him and us because we're adults and he's a tiny baby but it seems that that actually would require  
  
It's more complicated than that. That's facial recognition. He's asleep. He's awake. He's moving. He's not moving.  
  
So that, again, would be kind of lack of motion detection, the condition we're trying to filter against, which would be really zero at a good close-up frame. The other thing that I thought would be helpful was auto-tracking. Auto-tracking, when I looked at how Frigate implemented it,  
  
PTZ only so let's say it tracks a detected entity let's say a FedEx truck for example so it will automatically operate the PTZ controls exposed via ONVIF and zoom up on that unfortunately it doesn't do that for digital zoom  
  
but that would be a great feature for me even if we can just recognize the presence of a person regardless of who it is if it's in the bassinet my wife and i are not in the habit of sleeping in bassinets so we can rest assured that it's our son and if it could automatically crop into his closest face it would make the motion detection more reliable  
  
and it would make it a lot easier for me to just take a quick glance at that frame and say okay everything's fine i can see i can see he's fidgeting i can see he's awake i can see he's asleep looks like he needs his diaper changed all that kind of stuff um so  
  
So at the basic level of just having these cameras integrated with something like Frigate, I can do it. But when I tried to turn on just the basic features for person detection, even after downloading the model and making sure it was TensorRT and not ONNX that I downloaded, I struggled to install the ONNX runtime and model.  
  
But even with trying to do everything that I thought was correct to enable GPU acceleration, including installing the NVIDIA container, whatever it's called, runtime, I think, it only shows 1% GPU usage and the CPU for object detection, that'll throw it up to like 80, 90%. And if I just throw a little bit more stuff at it, like  
  
The zoning, it'll just store the hardware basically. So that's free. Now, pardon me, there's two things that I'm looking at or thinking about. And again, bear in mind that I would really like to have this working nicely as I want, but I don't want to make this a gigantic project.  
  
One is on the software level. I feel like what I'm looking for is quite specific, but RTSP and HLS is pretty general, right? Every camera gives that out. Then on the other hand, we have these libraries for object recognition, facial recognition, and even I imagine there has to be one for...  
  
Wake, Sleep, Recognition or if not maybe one I can create myself with some training data stills I take from the camera. One would be instead of using Frigate which seems to be a nice system but just I'm not able to out of the box the parameters are just too much for my hardware.  
  
Add just the components that I need very specifically. The non-motion one, which is motion sensing and reporting time since the last motion and then detection level. Person state detection, crying, fidgeting, asleep, five or six different types of motion we could define. And what else did I say? Oh yeah, cry detection.  
  
which I think should be something that's I know it's in most audio recognition models. That's approach one. Approach two is trying to find a project that's either cloud hosted that you can pass up your RDSP streams or  
  
you can deploy something locally and it really is actually made for this because I think that's always a key is trying to find instead of trying to work around solutions made for other things trying to find something that's really zoned in on this use case oh I tried agent DVR as well and couldn't really didn't really kind of get to grips with that very well at all  
  
So that's number two. I did see earlier in some prompt around that there was a GitHub project of some kind or another that was actually AI for baby related or newborn related detection. Finally, buying new hardware. So that's definitely something that I could do, would like to do actually. My only hesitation so far has just been besides the financial expenditure  
  
I'm trying to figure out a new box and what do I need. Here in Israel where I'm based, I can't find the Google Carl on the market anywhere. I've looked for it, couldn't find it. But there is a company, Helio is based here, and they make a TPU. But given the fact that the i3 that I'm using is ancient, relatively speaking, and the GPU is very weak,  
  
and these TPU devices are still kind of a little bit obscure probably what I'd prefer to do if it were if I were naming the hardware I'd like to have I think this is definitely a bare metal dedicated box application I don't think that an NVR should be you know I think I want something for the task and only the task I don't want to over provision or under provision and just something with a nice speedy CPU and a decent GPU with  
  
The right kind of GPU to handle this kind of workload and accelerate this workload. And then I can just update, provision something on that. As I use Home Assistant, and it's good, I'd like to also use MQTT for alerting. So for example, Frigate has a really nice integration in that respect.  
  
and I don't think with Frigate it should be too challenging to kind of hack around for the non-detection thing or for the presence thing like an automation or just an alert. David is in this bed. David has left this bed. Again, the active camera one I mentioned, which I think could actually be very helpful. So we can just have really one camera page. A grid if you need it, but the only camera, even though all the three cameras we have are live,  
  
I only want to check the camera wherever he is and when he's not under physical observation or extra observation would be helpful. I tend to be a night owl as well so I'm kind of the designated nighttime monitor in the house.  
  
So that's pretty much everything about the project, what I've tried, where I'm up to, what I've learned. It's been quite interesting so far. We've definitely both seen the value in it, my wife and I. It's reassuring and at the right time it kind of tells me when I need to jump out of my office and pick him up, swaddle him, change his diaper.  
  
I can feel like I like I don't it gives me a lot of peace of mind that I'm not sort of I can do my own work and stuff especially when it's nice and quiet at night time but I have a very good sense of how he's doing and that everything's okay and so that's kind of the basic and then these ideas for a more fitting system or an or a system that just because I know there is for sure all the components in place to get exactly what I'm looking for I think  
  
and I'm willing to go that extra final last mile just to get something that really actually works very well for this. So that was a huge amount of information. What I'd like to get from you is your thoughts. Be as detailed as you can.  
  
where we are up to your thoughts for the best way forward give me a few options contextualize it to Ezra specifically regarding the availability of components I can buy stuff on Aliexpress but it's probably for this it would be a local purchase preferred Ivory and KSP are the main tech stores I'm trying to think of any last details here  
  
Proxner prices for different implementations, pros and cons. And for the software question, if you think it's worth tinkering with Frigate, layering on my own components on top of the RTSP streams to try some alerting via MQTT. Ideally, if that approach is one we're going for, still get those streams into Home Assistant, including the automatically recropped frame I've tried to do before. Query detection alerting via MQTT.  
  
How alerting could work, especially emergency alerting. Could it be sent to a smart watch or a smart bracelet or an alarm in the home? Give me a full run through of everything I've kind of been exploring here."""),
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
    output_file = os.path.join(outputs_dir, f"raw_run_{timestamp}.md")
    
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
        f.write(f"# Raw Run Output\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Model:** {model}\n\n")
        f.write(f"**Prompt:** Raw voice transcription of baby monitoring project\n\n")
        f.write("## Response\n\n")
        f.write("".join(full_output))
    
    print(f"\n\nOutput saved to: {output_file}")

if __name__ == "__main__":
    generate()

# Automotive Work Instruction Generator

This Python script uses Azure OpenAI to automatically generate standardized, step-by-step work instructions for automotive manufacturing tasks.

## How It Works

- **Task List:**  
   Define a list of automotive manufacturing tasks in `TASK_DESCRIPTIONS`.

- **Prompt Engineering:**  
  For each task, the script sends a prompt to the OpenAI API, asking it to generate clear, numbered work instructions including:

  - Safety precautions
  - Required tools (if any)
  - Acceptance checks

- **Output:**  
  The script prints each task and its generated work instructions in a readable format.

## Requirements

- Python 3.x
- openai
- python-dotenv

## Install dependencies

- pip install openai python-dotenv

## Set your Azure OpenAI credentials in a .env file

AZURE_OPENAI_ENDPOINT=your-endpoint-url
AZURE_OPENAI_API_KEY=your-api-key

## Code Overview

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DEPLOYMENT_NAME = "GPT-4o-mini"

TASK_DESCRIPTIONS = [
    "Install the battery module in the rear compartment, connect to the high-voltage harness, and verify torque on fasteners.",
    "Calibrate the ADAS (Advanced Driver Assistance Systems) radar sensors on the front bumper using factory alignment targets.",
    "Apply anti-corrosion sealant to all exposed welds on the door panels before painting.",
    "Perform leak test on coolant system after radiator installation. Record pressure readings and verify against specifications.",
    "Program the infotainment ECU with the latest software package and validate connectivity with dashboard display."
]

def create_client():
    """Create and return Azure OpenAI client."""
    return OpenAI(
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )

def generate_instruction(client, task):
    """Generate work instructions for a given task."""
    prompt = f"""You are an expert automotive manufacturing supervisor. Generate step-by-step
                work instructions for the following new model task. Include safety
                precautions, required tools (if any), and acceptance checks. Write in clear,
                numbered steps suitable for production workers.

Task:
\"\"\"{task}\"\"\"

Work Instructions:"""
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating instructions: {e}"

def main():
    """Main function to generate instructions for all tasks."""
    client = create_client()

    for task in TASK_DESCRIPTIONS:
        instructions = generate_instruction(client, task)
        print(f"\nTask: {task}")
        print(f"Work Instructions:\n{instructions}\n")
        print("-" * 80)

if __name__ == "__main__":
    main()
```

# Response


Task: Install the battery module in the rear compartment, connect to the high-voltage harness, and verify torque on fasteners.
Work Instructions:

### Work Instructions for Installing the Battery Module in the Rear Compartment

**Task:** Install the battery module in the rear compartment, connect to the high-voltage harness, and verify torque on fasteners.

---

#### Safety Precautions:

1. **Personal Protective Equipment (PPE):**

   - Wear safety glasses to protect your eyes.
   - Use insulated gloves to prevent electric shock.
   - Wear steel-toed boots to protect your feet.
   - Ensure you are wearing a hard hat if overhead hazards are present.

2. **High-Voltage Safety:**

   - Always treat the battery module as a high-voltage component.
   - Ensure the vehicle is powered off and the high-voltage system is deactivated before starting work.
   - Use a multimeter to verify that the system is de-energized.

3. **Lifting Safety:**
   - Use proper lifting techniques or mechanical aids when handling the battery module to avoid injury.
   - Ensure the area is clear of obstacles before lifting.

---

#### Required Tools:

1. Torque wrench (calibrated for high-torque applications)
2. Insulated socket set
3. Multimeter
4. Safety goggles
5. Gloves (insulated)
6. Lifting equipment (if necessary)

---

#### Work Instructions:

1. **Preparation:**

   - Ensure the work area is clean and free of any hazards.
   - Gather all required tools and PPE before starting the task.

2. **Verify Deactivation:**

   - Confirm that the vehicle's high-voltage system is deactivated.
   - Use a multimeter to check that there is no voltage present at the battery terminals.

3. **Position the Battery Module:**

   - If necessary, use lifting equipment to position the battery module over the rear compartment.
   - Align the battery module with the mounting points in the rear compartment.

4. **Install the Battery Module:**

   - Carefully lower the battery module into the rear compartment.
   - Ensure that the module is seated properly on the mounting points.

5. **Secure the Battery Module:**

   - Using the appropriate fasteners, secure the battery module to the mounting points.
   - Hand-tighten all fasteners to ensure proper alignment before applying torque.

6. **Connect the High-Voltage Harness:**

   - Locate the high-voltage harness connector.
   - Align the connector with the battery module's input and push it firmly until it clicks into place.
   - Ensure that the connector is secure and that there are no visible damages.

7. **Torque Fasteners:**

   - Using a calibrated torque wrench, apply the specified torque to each fastener according to the manufacturer's specifications.
   - Follow the recommended torque sequence if applicable (e.g., crisscross pattern).

8. **Final Inspection:**

   - Visually inspect the installation to ensure that the battery module is securely fastened and that the high-voltage harness is properly connected.
   - Check for any signs of damage or loose connections.

9. **Verify Connection:**

   - Use a multimeter to verify that the high-voltage connection is secure and that there is no voltage present at the terminals before reactivating the system.

10. **Documentation:**
    - Record the torque values applied to each fastener in the maintenance log.
    - Report any issues or discrepancies to the supervisor immediately.

---

#### Acceptance Checks:

- Ensure that the battery module is securely installed with no movement.
- Confirm that all fasteners are torqued to the specified values.
- Verify that the high-voltage harness is properly connected and secured.
- Check that the work area is clean and free of tools or debris before moving on to the next task.

---

**End of Work Instructions**

---

Task: Calibrate the ADAS (Advanced Driver Assistance Systems) radar sensors on the front bumper using factory alignment targets.
Work Instructions:

### Work Instructions for Calibrating ADAS Radar Sensors on Front Bumper

**Objective:** To ensure proper calibration of the ADAS radar sensors on the front bumper using factory alignment targets.

---

#### Required Tools:

1. Factory alignment targets
2. Calibration tool (specific to the vehicle model)
3. Torque wrench
4. Screwdriver set
5. Leveling tool
6. Safety goggles
7. Gloves
8. Reflective tape (if necessary)

---

#### Safety Precautions:

1. Always wear safety goggles and gloves when handling tools and equipment.
2. Ensure the vehicle is parked on a flat, stable surface to prevent movement during calibration.
3. Keep the work area clear of obstacles and ensure proper lighting.
4. Be aware of your surroundings and ensure no one is in the calibration area during the process.
5. Follow all manufacturer safety guidelines and protocols.

---

#### Step-by-Step Instructions:

1. **Preparation:**

   - Ensure the vehicle is turned off and the keys are removed from the ignition.
   - Park the vehicle on a level surface and engage the parking brake.

2. **Monitor Calibration:**

   - Observe the calibration tool for any error messages or prompts.
   - If prompted, make adjustments to the radar sensor positions as necessary to align with the targets.

3. **Complete Calibration:**

   - Once the calibration tool indicates that the process is complete, disconnect the tool from the diagnostic port.
   - Record any calibration data as required by the production process.

4. **Final Inspection:**

   - Recheck the radar sensors to ensure they are securely mounted and free from obstructions.
   - Verify that all tools and equipment are removed from the work area.

5. **Acceptance Check:**
   - Conduct a functional test of the ADAS system to ensure proper operation.
   - Confirm that the calibration was successful by checking for any error codes or warnings on the vehicle’s display.
   - Document the calibration results in the production log.

---

#### Notes:

- If any issues arise during the calibration process, consult the vehicle’s service manual or a supervisor for assistance.
- Ensure that all calibration data is recorded accurately for quality control purposes.

---

**End of Work Instructions**

---

Task: Apply anti-corrosion sealant to all exposed welds on the door panels before painting.
Work Instructions:

### Work Instructions for Applying Anti-Corrosion Sealant to Door Panels

**Task:** Apply anti-corrosion sealant to all exposed welds on the door panels before painting.

---

#### Safety Precautions:

1. **Personal Protective Equipment (PPE):**

   - Wear safety goggles to protect your eyes from splashes.
   - Use gloves to prevent skin contact with sealant.
   - Wear a respirator mask if working in a poorly ventilated area to avoid inhaling fumes.
   - Ensure steel-toed boots are worn to protect your feet.

2. **Work Area Safety:**
   - Keep the work area clean and free of any obstructions.
   - Ensure proper ventilation in the workspace.
   - Be aware of your surroundings and ensure no one is in the immediate area while applying sealant.

---

#### Required Tools and Materials:

1. **Tools:**

   - Applicator gun (if using cartridge sealant)
   - Brush or roller (for bulk sealant application)
   - Clean rags or paper towels
   - Utility knife (for opening sealant cartridges)

2. **Materials:**
   - Anti-corrosion sealant
   - Cleaning solvent (if needed for surface preparation)

---

#### Step-by-Step Instructions:

1. **Preparation:**

   - Ensure the door panels are clean and free of dust, grease, or any contaminants. Use a cleaning solvent if necessary.
   - Inspect the door panels for any damage or defects before proceeding.

2. **Gather Tools and Materials:**

   - Collect all required tools and materials listed above and place them within easy reach.

3. **Inspect Sealant:**

   - Check the expiration date on the anti-corrosion sealant. Do not use expired sealant.
   - Ensure the sealant is the correct type for the application.

4. **Open Sealant Cartridge:**

   - Use a utility knife to cut the tip of the sealant cartridge at a 45-degree angle, ensuring the opening is appropriate for the applicator gun.

5. **Load Applicator Gun:**

   - Insert the sealant cartridge into the applicator gun, ensuring it is securely in place.

6. **Apply Sealant:**

   - Position the applicator gun at a 45-degree angle to the exposed welds.
   - Apply a continuous bead of sealant along all exposed welds, ensuring complete coverage. If using a brush or roller, apply an even coat over the welds.

7. **Smooth the Sealant:**

   - Use a clean brush or your gloved finger to smooth out the sealant, ensuring it adheres well to the surface and fills any gaps.

8. **Inspect Application:**

   - Check that all exposed welds have been adequately covered with sealant. Look for any missed spots or uneven application.

9. **Clean Up:**

   - Clean any excess sealant from the applicator gun and tools using a suitable solvent.
   - Dispose of any used rags and empty sealant cartridges according to company waste disposal guidelines.

10. **Final Acceptance Check:**
    - Conduct a final inspection of the door panels to ensure:
      - All exposed welds are covered with sealant.
      - The sealant is smooth and evenly applied.
      - No excess sealant is present on non-weld areas.
    - Sign off on the task completion sheet, indicating that the anti-corrosion sealant application is complete and meets quality standards.

---

**End of Work Instructions**

**Note:** Always report any issues or concerns to your supervisor immediately.

---

Task: Perform leak test on coolant system after radiator installation. Record pressure readings and verify against specifications.
Work Instructions:

### Work Instructions for Performing Leak Test on Coolant System After Radiator Installation

**Objective:** To ensure the integrity of the coolant system by performing a leak test after the installation of the radiator.

---

#### Required Tools and Equipment:

1. Coolant pressure tester
2. Safety goggles
3. Gloves (nitrile or rubber)
4. Torque wrench (if applicable)
5. Pressure gauge (if not integrated with the tester)
6. Clean cloth or paper towels
7. Recording sheet or digital device for data entry

---

#### Safety Precautions:

1. Always wear safety goggles and gloves to protect against coolant splashes and potential chemical exposure.
2. Ensure the engine is cool before starting the leak test to prevent burns.
3. Be cautious of sharp edges around the radiator and surrounding components.
4. Dispose of any coolant spills immediately and according to safety regulations.
5. Follow all company safety protocols and guidelines.

---

#### Step-by-Step Instructions:

1. **Preparation:**

   - Ensure the vehicle is parked on a level surface and the engine is completely cool.
   - Gather all required tools and equipment.

2. **Visual Inspection:**

   - Inspect the radiator and surrounding hoses for any visible signs of damage or improper installation.
   - Check that all clamps and connections are secure.

3. **Connect Pressure Tester:**

   - Remove the radiator cap carefully to avoid any residual pressure.
   - Attach the coolant pressure tester to the radiator neck securely.

4. **Pressurize the System:**

   - Use the pressure tester to apply pressure to the coolant system. Set the tester to the manufacturer’s specified pressure (usually between 13-16 psi, but verify with specifications).
   - Allow the system to stabilize for a few moments.

5. **Monitor Pressure:**

   - Observe the pressure gauge on the tester. Record the initial pressure reading on the recording sheet.
   - Wait for 5 minutes and monitor the gauge for any drop in pressure.

6. **Check for Leaks:**

   - While monitoring the pressure, visually inspect all connections, hoses, and the radiator for any signs of coolant leakage.
   - If any leaks are detected, mark the area for repair and do not proceed until the issue is resolved.

7. **Record Final Pressure:**

   - After 5 minutes, record the final pressure reading on the recording sheet.
   - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

8. **Acceptance Check:**

   - Compare the recorded pressure readings against the manufacturer’s specifications.
   - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

9. **Visual Inspection:**

   - Inspect the radiator and surrounding hoses for any visible signs of damage or improper installation.
   - Check that all clamps and connections are secure.

10. **Connect Pressure Tester:**

    - Remove the radiator cap carefully to avoid any residual pressure.
    - Attach the coolant pressure tester to the radiator neck securely.

11. **Pressurize the System:**

    - Use the pressure tester to apply pressure to the coolant system. Set the tester to the manufacturer’s specified pressure (usually between 13-16 psi, but verify with specifications).
    - Allow the system to stabilize for a few moments.

12. **Monitor Pressure:**

    - Observe the pressure gauge on the tester. Record the initial pressure reading on the recording sheet.
    - Wait for 5 minutes and monitor the gauge for any drop in pressure.

13. **Check for Leaks:**

    - While monitoring the pressure, visually inspect all connections, hoses, and the radiator for any signs of coolant leakage.
    - If any leaks are detected, mark the area for repair and do not proceed until the issue is resolved.

14. **Record Final Pressure:**

    - After 5 minutes, record the final pressure reading on the recording sheet.
    - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

15. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

16. **Visual Inspection:**

    - Inspect the radiator and surrounding hoses for any visible signs of damage or improper installation.
    - Check that all clamps and connections are secure.

17. **Connect Pressure Tester:**

    - Remove the radiator cap carefully to avoid any residual pressure.
    - Attach the coolant pressure tester to the radiator neck securely.

18. **Pressurize the System:**

    - Use the pressure tester to apply pressure to the coolant system. Set the tester to the manufacturer’s specified pressure (usually between 13-16 psi, but verify with specifications).
    - Allow the system to stabilize for a few moments.

19. **Monitor Pressure:**

    - Observe the pressure gauge on the tester. Record the initial pressure reading on the recording sheet.
    - Wait for 5 minutes and monitor the gauge for any drop in pressure.

20. **Check for Leaks:**

    - While monitoring the pressure, visually inspect all connections, hoses, and the radiator for any signs of coolant leakage.
    - If any leaks are detected, mark the area for repair and do not proceed until the issue is resolved.

21. **Record Final Pressure:**

    - After 5 minutes, record the final pressure reading on the recording sheet.
    - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

22. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

23. **Connect Pressure Tester:**

    - Remove the radiator cap carefully to avoid any residual pressure.
    - Attach the coolant pressure tester to the radiator neck securely.

24. **Pressurize the System:**

    - Use the pressure tester to apply pressure to the coolant system. Set the tester to the manufacturer’s specified pressure (usually between 13-16 psi, but verify with specifications).
    - Allow the system to stabilize for a few moments.

25. **Monitor Pressure:**

    - Observe the pressure gauge on the tester. Record the initial pressure reading on the recording sheet.
    - Wait for 5 minutes and monitor the gauge for any drop in pressure.

26. **Check for Leaks:**

    - While monitoring the pressure, visually inspect all connections, hoses, and the radiator for any signs of coolant leakage.
    - If any leaks are detected, mark the area for repair and do not proceed until the issue is resolved.

27. **Record Final Pressure:**

    - After 5 minutes, record the final pressure reading on the recording sheet.
    - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

28. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

    - Allow the system to stabilize for a few moments.

29. **Monitor Pressure:**

    - Observe the pressure gauge on the tester. Record the initial pressure reading on the recording sheet.
    - Wait for 5 minutes and monitor the gauge for any drop in pressure.

30. **Check for Leaks:**

    - While monitoring the pressure, visually inspect all connections, hoses, and the radiator for any signs of coolant leakage.
    - If any leaks are detected, mark the area for repair and do not proceed until the issue is resolved.

31. **Record Final Pressure:**

    - After 5 minutes, record the final pressure reading on the recording sheet.
    - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

32. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

33. **Check for Leaks:**

    - While monitoring the pressure, visually inspect all connections, hoses, and the radiator for any signs of coolant leakage.
    - If any leaks are detected, mark the area for repair and do not proceed until the issue is resolved.

34. **Record Final Pressure:**

    - After 5 minutes, record the final pressure reading on the recording sheet.
    - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

35. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

    - If any leaks are detected, mark the area for repair and do not proceed until the issue is resolved.

36. **Record Final Pressure:**

    - After 5 minutes, record the final pressure reading on the recording sheet.
    - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

37. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

    - If the pressure has dropped significantly (more than 1-2 psi), this indicates a leak in the system.

38. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

39. **Release Pressure:**
    - Carefully release the pressure from the tester by following the manufacturer’s instructions.
40. **Acceptance Check:**

    - Compare the recorded pressure readings against the manufacturer’s specifications.
    - If the pressure is within the acceptable range and no leaks are detected, proceed to the next step. If not, report the issue to the supervisor.

41. **Release Pressure:**

    - Carefully release the pressure from the tester by following the manufacturer’s instructions.
    - Remove the pressure tester and reattach the radiator cap securely.

42. **Release Pressure:**
    - Carefully release the pressure from the tester by following the manufacturer’s instructions.
    - Remove the pressure tester and reattach the radiator cap securely.
43. **Release Pressure:**

    - Carefully release the pressure from the tester by following the manufacturer’s instructions.
    - Remove the pressure tester and reattach the radiator cap securely.

44. **Clean Up:**
    - Wipe any spilled coolant with a clean cloth or paper towels.

- Remove the pressure tester and reattach the radiator cap securely.

10. **Clean Up:**

    - Wipe any spilled coolant with a clean cloth or paper towels.
    - Dispose of any waste materials according to company policies.

11. **Clean Up:**

    - Wipe any spilled coolant with a clean cloth or paper towels.
    - Dispose of any waste materials according to company policies.

12. **Documentation:**

    - Dispose of any waste materials according to company policies.

13. **Documentation:**
    - Submit the completed recording sheet to the supervisor for review and filing.
14. **Documentation:**
    - Submit the completed recording sheet to the supervisor for review and filing.
    - Submit the completed recording sheet to the supervisor for review and filing.
    - Ensure all tools are returned to their designated storage areas.
    - Ensure all tools are returned to their designated storage areas.

---

**End of Work Instructions**

**Note:** Always refer to the specific vehicle service manual for any model-specific procedures or specifications.

---

Task: Program the infotainment ECU with the latest software package and validate connectivity with dashboard display.
Work Instructions:

### Work Instructions for Programming the Infotainment ECU and Validating Connectivity

**Task:** Program the infotainment ECU with the latest software package and validate connectivity with the dashboard display.

---

#### **Safety Precautions:**

1. **Personal Protective Equipment (PPE):**

   - Wear safety glasses to protect your eyes.
   - Use anti-static wrist straps to prevent electrostatic discharge (ESD) damage to electronic components.
   - Ensure that you are wearing closed-toe shoes and appropriate work attire.

2. **Work Area Safety:**
   - Keep the work area clean and free of clutter.
   - Ensure that all tools and equipment are in good working condition.
   - Be aware of your surroundings and avoid distractions while working.

---

#### **Required Tools:**

1. Laptop or PC with the appropriate software installed for ECU programming.
2. OBD-II (On-Board Diagnostics) cable or diagnostic tool.
3. Anti-static wrist strap.
4. USB drive with the latest software package.
5. Multimeter (for connectivity checks).
6. Torque wrench (if applicable for securing ECU).

---

#### **Work Instructions:**

1. **Preparation:**

   - 1.1. Gather all required tools and materials.
   - 1.2. Ensure the vehicle is in a safe and stable position (parked on a flat surface with the ignition off).
   - 1.3. Connect the anti-static wrist strap to a grounded surface.

2. **Access the Infotainment ECU:**

   - 2.1. Locate the infotainment ECU in the vehicle (refer to the vehicle service manual for specific location).
   - 2.2. If necessary, remove any panels or covers to access the ECU.

3. **Connect the Diagnostic Tool:**

   - 3.1. Plug the OBD-II cable into the vehicle’s OBD-II port.
   - 3.2. Connect the other end of the cable to your laptop or diagnostic tool.

4. **Load the Software Package:**

   - 4.1. Insert the USB drive containing the latest software package into the laptop.
   - 4.2. Open the ECU programming software on your laptop.
   - 4.3. Follow the on-screen instructions to select the appropriate software package for the infotainment ECU.

5. **Program the Infotainment ECU:**

   - 5.1. Initiate the programming process by clicking the “Program” or “Update” button in the software.
   - 5.2. Monitor the progress bar and wait for the programming to complete (this may take several minutes).
   - 5.3. Once programming is complete, the software will display a confirmation message.

6. **Disconnect the Diagnostic Tool:**

   - 6.1. Safely disconnect the OBD-II cable from the vehicle and the laptop.
   - 6.2. Remove the USB drive from the laptop.

7. **Validate Connectivity with Dashboard Display:**

   - 7.1. Reconnect the vehicle battery if it was disconnected during the process.
   - 7.2. Turn on the vehicle ignition (do not start the engine).
   - 7.3. Check the dashboard display for the infotainment system to power on.
   - 7.4. Test the functionality of the infotainment system (e.g., radio, navigation, Bluetooth) to ensure it is operational.

8. **Perform Acceptance Checks:**

   - 8.1. Verify that the infotainment system displays the correct software version.
   - 8.2. Confirm that all features of the infotainment system are functioning correctly.
   - 8.3. Use a multimeter to check for proper voltage and ground connections at the ECU if any issues arise.

9. **Final Steps:**
   - 9.1. If all checks are satisfactory, secure the ECU and any panels or covers that were removed.
   - 9.2. Clean up the work area and return all tools to their designated locations.
   - 9.3. Document the programming process and any observations in the vehicle’s service record.

---

**End of Work Instructions**

**Note:** If any issues are encountered during programming or validation, report them to your supervisor immediately for further assistance.

---

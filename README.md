# Installation
```bash
git clone [this repo]
cd Pupper-V2-Interface
pip3 install -e .
```

# Run example
Before running the code, turn on robot and wait for it to complete its homing sequence. 
The example will move the actuators softly to their 0.0 angles which corresponds to the configuration where the legs are pointing straight down. I recommend putting the robot on a block so it doesn't tip over when this happens. Or change the position command inside the code.
```bash
cd examples
python3 command_and_query.py
```

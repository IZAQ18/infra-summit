# Third-party resources

The simulator uses the SO-101 model and meshes from
[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100/tree/eecbe3e0a9ebb23e25ad7b2759b03884c6660903/Simulation/SO101),
revision `eecbe3e0a9ebb23e25ad7b2759b03884c6660903`, under Apache-2.0.
The upstream license is preserved in `licenses/SO-ARM100-Apache-2.0.txt`.
`simulation/upstream_manifest.json` records source paths, byte counts and SHA-256 hashes.
The downloader keeps the original model, meshes and license in ignored `.cache/so101`.

LineProof's scene composer modifies the model in memory: it creates two copies,
prefixes body/joint/site/actuator names, changes base placement and orientation,
and adds a table, primitive objects, lighting and two cameras. It retains upstream
joint ranges, inertia, actuator gains and collision geometry. The starting joint
pose is changed to avoid inter-arm intersection. These are engineering experiments,
not a certified digital twin or a validated dinner-task environment.

MuJoCo, LeRobot, PyTorch, torchvision and OpenVINO are installed from their official
package indexes; their original licenses remain with the installed packages.
LineProof does not redistribute their source or weights. The ACT runtime probe
initializes random parameters and deliberately downloads no learned weights.

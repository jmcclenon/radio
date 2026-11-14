# Lion's Den

One-page internet radio for reggae, dub, jazz, classical and other stations.

Live at https://jmcclenon.github.io/radio/

## AI radio finder (preview)

An optional, self-contained agent skill is being developed under [skills/lions-den-radio-finder](skills/lions-den-radio-finder/SKILL.md). It searches the Radio Browser community directory and helps listeners find stations to open in the existing website. It **does not** remotely start playback, and no skill has been listed for sale yet.

Quick test from the repository root (Python 3, no third-party packages):

```bash
python3 skills/lions-den-radio-finder/scripts/find_stations.py --query reggae --field tag --country JM --limit 5
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The script queries the public Radio Browser directory. Playback is controlled by the user within Lion's Den. Station availability is provided by third parties.

See [the proposed marketplace plan](docs/AGENSI-LAUNCH.md) for positioning and constraints.

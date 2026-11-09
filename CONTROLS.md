# Controls

Run `python main.py` from this directory. The logo leads to the title.

| Screen | Key | Action |
| --- | --- | --- |
| Title | Space | Start a new game |
| Title | Esc | Quit |
| Play | Left / Right | Move |
| Play | Space | Fire selected ball (wake up first if sleeping) |
| Play | P | Pause |
| Pause | P | Resume |
| Play | I | Open item selection and freeze play |
| Items | 1 | Select small ball and resume |
| Items | 2 | Select large ball and resume |
| Items | 0 | Disable new shots and resume |
| Items | I / Esc | Resume without changing selection |
| Play | Esc | Return to title |

New games start with the small ball. Selection does not remove balls already
in flight. The item screen uses `item_select.png`. Closing the window quits.

Headless behavior checks: `python -B test_item_modes.py`.

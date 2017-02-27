# mbed_automat
## command line tool intended to augument mbed web compiler workflow.
tested on win10, will work on \*nix with minor changes. Or it might work right out of the box, I don't know how [**glob**](https://docs.python.org/3/library/glob.html#glob.glob) modules behave on \*nix.

* Program runs in constant loop, looking for a specifed filename (*<yourText>*.bin) in specified folder.

* If there is something present (downloaded by mbed online compiler), it beeps (*warning* beep) and performs action specific to the board. Board recognition is done my mean of searching for known board name in the <yourText>. You are free to add your own boards cases. When done, beeps (*during* beep).

* As a next step it moves the file ([**shutil**](https://docs.python.org/3/library/shutil.html#shutil.move) package) to the board and beeps (*finished* beep).

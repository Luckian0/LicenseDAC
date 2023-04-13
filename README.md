
# LicenseDAC

LicenseDAC offers an advanced search in files and archives to detect all the licenses that apply in the respective source code. With the help of the GUI interface, it is very easy to read the result. Also detect the primary programming language and the release date.


## Getting it

LicenseDAC requires Python 3 or newer versions.
Use ```deep_translator``` to help translate text, so please install it.
```pip install -U deep-translator```
Also, please install the following patch:
```pip install pygments``` for detecting programming languages


## Getting Started

Here is a very simple tutorial of how you can use this app.

By pressing the ```Select zip``` button, an explorer window will open where you can select the desired file (it can be in the following formats: .zip; .tar.gz; .tar.bz2, etc.), after selection you will be automatically initiates the unzipping process followed by the searching process

If a format is not supported (ex: ```source.jar```), a log message will appear informing you that the source code must be unzipped manually.

If you want to search in a source code that is already unzipped on your device, all you have to do is use the ```Select Directory``` button to load the file and then the ```License Search``` button to start the search.

The selected folder is displayed in the field below the search buttons.

Under this field, you can follow the search process, which appears as a LOG-type message. After the search is completed, the message Done will appear, and below this field will appear the licenses found after your search. By clicking on a ```license button``` in the field above, the files in which the respective license was found will appear. Double-click on the ```desired file``` to open in the window on the right, where you can see how many times the respective license was found in that file through the ```buttons``` that appear on the bottom of the screen and are numbered from ```1``` to ```-n```; clicking on one of the ```buttons``` will focus on the line where the license was found.

At the bottom, under the text, if there is another license in that file apart from the selected one, the other licenses will appear in the form of ```buttons```. Clicking on one of those ```buttons``` below will show how many times that additional license was found in that file. Click on one of the ```numbers``` to focus on the line where that hint appears.

In the window in which the file opens, you can do the following by right-clicking the mouse:
- Opening the selected links (you have to select the link and then press the right click followed by choosing the option ```Open URL```).
- Translation of the selected text (by default, the language in which it is translated is English, but you can choose one of the other languages through the drop-down list button; select the text you want to translate and then press the right click followed by choosing the option ```translate```).
- ```Correction``` on the found licenses  !!! Use with caution!!! (If a result is wrong, you can apply a correction in the future by selecting the word or phrase you want to be ignored in the future; do not select more than one line; it will not apply in the future.) If no word is selected or less than 4 characters are selected, a warning window will appear. The correction will be applied to the license that was selected by pressing the license button, and another license can`t be chosen to apply that correction. If you are on the ```Unknow``` license tab, after selecting the text and pressing the ```add``` button from the pop-up menu, you have the option to choose that phrase (word) to apply either inside a line or to match with the whole line. With the ```Check``` option, you can check the file where all the phrases (words) that will be ignored in the future have been stored. Be careful, if you make changes in this file you must remember that each phrase (word) is between '|||', do not leave '|||' at the beginning or at the end, this will make it impossible to find that license in the future
- Search in the open file (by pressing the ```Find``` button or the ```Ctrl. + F``` buttons on the keyboard, a window will appear from which you can search for the desired word; you also have the option ```Ignore Case```
- The ```Search``` option will open a Google page in your browser and search for the selected phrase.
- The ```Open File``` function will open the respective file in the Notepad application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Feedback

If you have any feedback, please reach out to me at FlorinelBejinaru@Gmail.com


## License and Copyright

LicenseDAC is copyright © Florinel Bejinaru 
It is licensed under GPL v3.


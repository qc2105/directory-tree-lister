# Directory Tree Lister

Creates a recursive list of a directory and outputs to either an excel file and or a text file. Windows and MacOS/Linux 
supported.

## Usage

### Using the core script

> dtlister/core.py

```
$ python dtlister/core.py  
$ Input a directory for scanning: /Users/johnsmith/Movies
$ Input a directory for output file: /Users/johnsmith/Documents

$ Select output type:
$ 1) Text - .txt
$ 2) Excel - .xlsx

$ 1

$ Directory Tree created in text file: directory-tree-Movies.txt
$ In Directory: /Users/johnsmith/Documents
```

### Notes about the GUI option

The project builds successfully on MacOS 10.12.2, though it should build successfully on Windows as well. There are 
some small notes regarding this in `resources/build-notes.txt`.


### Building on MacOS via cx_freeze

`python setup.py bdist_mac --custom-info-plist resources/Info.plist --iconfile resources/icon.icns`


## Authors

* **spottywolf**

See also the list of [contributors](https://github.com/spottywolf/mathfever/graphs/contributors) who participated in 
this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
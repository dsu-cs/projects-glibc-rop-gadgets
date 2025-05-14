# Glibc ROP Gadget Autocomplete

This repository contains the source code for a web app designed to mitigate the difficulty that those working in software exploitation face when attempting to build ROP chains in software running on remote machines that are using different versions of glibc than what is present/compiled on the exploiter's host machine. The web app provides a quick and straightforward way to search for ROP gadgets within different versions of glibc compiled for different architectures. The app features Trie based autocomplete features, as well as AVL Tree based sorting of ROP gadget suggestions. 

## Project Files

- `index.html`: The HTML structure for the web app.

- `styles.css`: The styling for the web app.

- `script.js`: The JavaScript code that implements the Trie and AVL Tree data structures and handles the web app's logic.

- `update_source_files.py`: A python3 script that is intended to be used to update index.html when new glibc ROP gadget text files are added for additional versions/architectures.
  
  ###### NOTE: the repository also contains a number of other .txt files with filenames of the format [arch]-[version].txt. These are text files containing ROP gadget instructions (intended to contain the ropper output from a specific binary executable, in this case libc.so.6, for their respective versions). Each line contains a hexadecimal address followed by the corresponding instruction. The ROP gadget instructions were determined using the tool Ropper, which can be found at https://github.com/sashs/Ropper

## Features

- **Search multiple versions of glibc**: ROP gadgets from several versions of glibc compiled for multiple architectures are available for searching. Additional versions/architectures can easily be added using the included "update_source_files.py" python script. 
- **Autocomplete functionality**: The app provides real-time autocomplete suggestions as you type, using a Trie to efficiently search through the list of ROP gadget instructions from a given version of glibc compiled for a particular architecture.
- **ROP gadget sorting**: When searching, the app uses an AVL Tree data structure to quickly/efficiently sort ROP gadgets from shortest to longest, ensuring a smooth workflow for potential users.
- **Responsive design**: The web app is styled to be responsive, ensuring a good user experience on different screen sizes.
- **Python script for easy incorporation of new source files**: The included python script can be used in conjunction with roppper to quickly add additional ROP gadget source lists from versions of glibc not included in this repository.

## How to Use

1. Clone this repository to your local machine:
   `git clone https://gitlab.com/csc3104/hw5_tries`

2. Open the `index.html` file in your web browser (or spin up a local python web server with ```bash python -m http.server``` and navigate to localhost:8000) to run the web app.

3. Select a "glibc version" and an "architecture" from the radio button options.

4. Start typing in the input field, and the app will suggest matching ROP gadget instructions from the appropriate source file.

5. Click on a specific gadget in the search results to copy (1) the address to your clipboard, and (2) the gadget to the search bar. 

6. (Optional) Download additional glibc binary versions compiled for other architectures, use Ropper to store ROP gadgets to a .txt file, and use update_source_files.py to add them to the web app. For example, if you have a binary for glibc 2.29 compiled for i386 architecture (usually named "libc.so.6"), you can add it to the web app by running the following commands:
   
   ```bash
   ropper --nocolor -f libc.so.6 > i386-2.29.txt 
   python3 update_source_files.py
   ```

## Code Explanation

### `index.html`

The main HTML file that contains the structure of the web app, including an input field for autocomplete and a results list to display suggestions. The `styles.css` file is linked for styling, and `script.js` is included for the functionality.

### `styles.css`

This file contains the styling for the web app, ensuring it looks clean and is responsive. The body is centered, and the input field is styled for a better user experience.

### `script.js`

This file contains the logic for the Trie data structure and the autocomplete functionality:

- **TrieNode**: Represents a node in the Trie, storing its children, a flag indicating if it's the end of a word, and an address for ROP gadgets.
- **Trie**: Implements the Trie with methods for inserting new instructions and searching for matches based on a prefix. Search() method uses AVL Tree to sort matched instructions from shortest to longest.
- **AVLNode**: Represents a node in the AVL Tree, storing its children, data, and the height of the node.
- **AVLTree**: Implements the AVL Tree with methods for getting and updating the height of the tree, getting the balance factor, inserting, various rotations, and a standard in-order-traversal.
- **Autocomplete logic**: The script listens for user input and shows matching results from the Trie. It also handles loading data from `data.txt` and displaying the results in a list format.

## Acknowledgments and Use of Large Language Models

- A variety of resources were used in the completion of this repository including, but not limited to The Linux Code and Geeks For Geeks. Where applicable, these resources have been referenced in the source code comments.

- The original idea for this project was inspired by a discussion I had with Dr. Andrew Kramer and was produced for a class taught by Dr. John Hastings (both at Dakota State University). I am deeply indebted to them both for their insights and suggestions with regard to this project.

- Binaries for various versions of glibc compiled for different architechtures were downloaded from the Ubuntu repository at https://packages.ubuntu.com/

- The ROP gadget instructions were determined using the tool Ropper, which can be found at https://github.com/sashs/Ropper

- ChatGPT was used to generate the template for this README document, given the following prompt:
  
  > Please give me a the markdown code for a github style README.md file for a repository containing the following files: index.html, styles.css, script.js, and data.txt.

- ChatGPT was used to generate the base code for the Trie object (although I modified it to fix errors and fit my designs better, see code comments) and WebApp interface, given the following prompt:
  
  > Please give me the code (html, javascript, css, etc) for a simple web app that will use a trie data structure to quickly autocomplete one of possibly many Unicode lines stored in a text file (data.txt) in the same directory. The lines may contain space characters, and the trie should account for this. The web app should display a drop-down list of possible matches as soon as the user begins typing.

- ChatGPT was used to generate the base code for the AVL Tree object (although I modified it to fix errors and fit my designs better, see code comments), given the following prompt:

  > Please provide me with the code for a javascript implimentation of an AVL tree

- DeepSeek was used to add functionality/logic to pull data from various source files given the following prompt:

  > I would like to extend this web application to give the user the option to specify which version(s) of glibc to use as well as the architecture. Please adjust the source code so that there are checkboxes for various options for both of these catagories which the user can select before searching. I would like you to include 2.35 and 2.39 for the "versions" check boxes; and amd64 and i386 for the "architectures" check boxes. I will likely expand these later.

 >The application should no longer pull rop-gadgets from "data.txt" but instead should determine the correct text file name based on the check boxes marked by the user. For example, if the user checks the boxes for amd64 and 2.35, then the file to search for rop-gadgets should be set to "amd64-2.35.txt". If the user selects more than one architecture and/or version, then the application should simply default to one version and one architecture for now (I will likely add the capability to search multiple files at a later time).

## License

This repository is for educational purposes only. Feel free to modify and use the code as needed.

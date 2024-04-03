
# Freestyle Helper App

Welcome to the Freestyle Helper App's GitHub repository! This innovative application, designed using Python, leverages the Pygame library for rendering visuals and Tkinter for dialog-based user interaction. Its primary purpose is to aid freestyle artists in their practice sessions by providing random words to rhyme with, and enabling the addition, edition, and deletion of rhymes for each word.

#### Features

- **Dynamic Word Display**: Switch between a timed mode for automatic word changes and an on-demand mode to navigate words manually.
- **Rhyme Management**: Add, edit, and delete rhymes for the displayed word using intuitive Tkinter dialog boxes.
- **Data Persistence**: Words are loaded from a text file, and rhymes are managed in separate text files, ensuring your additions and changes are saved across sessions.

#### Installation

1. **Prerequisites**:
   - Ensure you have Python installed on your system (version 3.6 or higher recommended).
   - Pygame and Tkinter must be installed. You can install Pygame using pip:
     ```
     pip install pygame
     ```

     Tkinter usually comes with Python, but if you need to install it, refer to the official Tkinter documentation for your platform.

2. **Clone the Repository**:
   - Use Git to clone this repository to your local machine:
     ```
     git clone https://github.com/vknaut/FreestyleApp.git
     ```
   
3. **Run the Application**:
   - Navigate to the cloned repository's directory.
   - Run the application using Python:
     ```
     python freestyle_helper_app.py
     ```

#### Usage

- **Starting the App**: Upon launch, the application displays a random word from the loaded list and any associated rhymes.
- **Navigating Words**: Press the "New Word" button or use the left and right keys to change the displayed word.
- **Adding Rhymes**: Click "Add Rhyme" and enter your rhyme in the dialog box.
- **Editing Rhymes**: Select "Edit Rhyme", choose the rhyme to edit, and enter the new version.
- **Deleting Rhymes**: Click "Delete Rhyme" and select the rhyme you wish to remove.
- **Timed Mode**: Activate or deactivate the timed mode by pressing 'm'. Pause or resume the display of words in this mode with the spacebar.

#### Contributing

We welcome contributions from the community, whether it's in the form of bug reports, feature requests, or direct code contributions. Please read through our contribution guidelines before submitting your contributions.

#### License

This project is licensed under the MIT License - see the LICENSE file for details.

#### Support

If you encounter any issues or have questions about the application, please file an issue on this GitHub repository.

---

Happy Freestyling! 🎤✨

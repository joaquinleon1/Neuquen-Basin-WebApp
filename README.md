# Neuquén Basin WebApp
#### Video Demo:  https://youtu.be/7RpjFBfgTJE
## Description

The Neuquén Basin WebApp is designed to enhance the geological exploration experience of the Neuquén Basin by allowing users to not only find detailed information about geological formations but also to view geographic distributions through interactive maps. By providing easy access to bibliographic references, the app supports further research and serves as a valuable resource for both academics and professionals in the field of geology.

The platform is built using Flask, a micro-framework well-suited for the rapid development of web applications. The app utilizes SQLite for local database management, ensuring portability and simplicity, with easy setup and maintenance. This tool allows researchers to more efficiently manage geological data and references, facilitating more informed decisions in exploration and study.

## Features

- Search Geological Units: Find geological units that match user-defined properties like age, lithology, porosity, permeability, and more.
- View Properties: View detailed properties of specific geological formations, including thickness, TOC (Total Organic Carbon), and structural features, with relevant bibliographic references.
- Interactive Maps: Explore both outcrop locations and geological morphostructures of the Neuquén Basin, with information-rich pop-ups for further learning.

## Requirements

- Python 3.x
- Flask
- CS50 Python Library
- SQLite

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/geological-units-database.git
   cd geological-units-database

2. Set up the SQLite database: Ensure that you have the geological_units.db file in the root directory of the project. This database should contain the geological_units and formation_bibliography tables with the relevant data.

3. Run the application:
    ```bash
    flask Run

4. Open your browser and go to http://127.0.0.1:5000 to access the app.

## Endpoints

The application uses Bootstrap for styling, and the pages follow a layout with a header (navigation bar) and footer. The footer contains extra information like contact, rights, and terms.

#### Home
/ - The homepage of the application, featuring a carousel of images showcasing the principal outcrops of the basin. Each image links to the main functionalities of the app.

#### About
/about - Provides information about the application, its purpose, and key features of the Neuquén Basin. Includes AOS fade animations for dynamic presentation, and tooltips on key terms for enhanced user experience. Some images are clickable for more details.

#### Find Geological Units
/find_unit - Allows users to search for geological units based on specific properties such as thickness, TOC, and more. Below each input field, helpful descriptions are provided. All fields, except for TOC and Thickness, accept text input.

TOC and Thickness can be entered as a number or a range. The app compares the user input with the database range, whether it's a single value or a range.
If a match is found, users are redirected to the /matching_units page. If no matches are found, the /no_matches page is shown, displaying the user inputs.


#### View Formation Properties
/view_properties - Displays detailed properties of a selected geological formation from a dropdown list based on Javascript. Users can also type in the field to filter the list.

#### Individual Formation
/properties/<formation_name> - Displays detailed properties of a specific geological formation in a table format. The corresponding bibliography for the unit is also shown at the bottom.

#### All Geological Units
/all_units - Displays a list of all geological units available in the database. Each unit is presented in a card-style layout with a link to its properties page.

#### Interactive Map
/interactive_map - Displays a morphostructural map of the Neuquén Basin. The map features clickable icons that represent regions of the basin. When clicked, a pop-up provides additional information about the region.

#### Outcrops Map
/outcrops - Displays a map of the principal geological outcrops in the Neuquén Basin. Icons mark the location of each outcrop, and clicking on them opens a pop-up with an image and more information about the outcrop.

## Usage Examples

1. **Searching for a geological unit:**
   To search for geological units with a specific TOC value, go to `/find_unit` and enter the desired TOC range. For example, in the database, a certain unit could have:
   - TOC_min: 1.0
   - TOC_max: 3.0

   In `\find_unit` you will have a single field to complete for that property:
   - TOC

   Suppose you enter `4`. This input will not match with the above unit. However, an input of `3` or `2` would match.

   If any matching geological units are found, you’ll be redirected to `/matching_units`. In this case, the user would be allowed to follow a link to the properties table.

2. **Viewing formation properties:**
   Select a formation from the dropdown in the `/view_properties` page to see detailed properties like age, lithology, and more, including the bibliography.

3. **Interactive Maps:**
   On /interactive_map and /outcrops_map, users can interact with icons referenced over a map of the Neuquén Basin.


## Database Structure
The application uses an SQLite database (geological_units.db) with the following tables:

#### geological_units
- formation: Name of the geological formation.
- thickness_min, thickness_max: Thickness range of the formation.
- TOC_min, TOC_max: TOC (Total Organic Carbon) range for the formation.
- Others: age, lithology, porosity, permeability, structural_features, hydrocarbon_potential, paleoenvironment.

Note: in the database there is min and max values for the thickness and TOC properties, both are transformed on a single value column that consist in the range between min and max, separated by "-". As is has been said above, user can input a range or a single number, that would be compared with the range.

#### formation_bibliography
- formation: Name of the geological formation.
- bibliography: Bibliographic references for the formation.

## Contributing
We welcome contributions to improve the Neuquén Basin WebApp! You can get involved with the coding:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Test your changes.
5. Submit a pull request describing your changes.

Furthermore, the database could be improved. Types of Contributions:

1. Adding New Geological Units
2. Updating Existing Data
3. Adding Bibliographic References

Steps to Contribute Data:

1. Fork the Repository: Start by forking this repository to your own GitHub account. This will create a copy of the repository where you can work freely without affecting the original project.

2. Clone Your Fork: Clone your fork to your local machine:

```bash
    git clone https://github.com/yourusername/neuquen-basin-webapp.git
    cd neuquen-basin-webapp
```

3. Set Up the Database Locally: Ensure that you have the geological_units.db file set up in your local environment. This file contains the database structure where you will be adding or updating geological units.

4. Modify the Database: You can use SQLite tools to add or modify the entries in the database. Here are some steps to guide you:

5. Add Geological Units.

6. Update Existing Geological Units.

7. Add Bibliographic References.

8. Testing: After making your changes, run the application locally to ensure everything works as expected. Verify that the new or updated data is displayed correctly in the app.

9. Commit Your Changes: Once you’ve made your modifications, commit the changes to your fork:

```bash
git add geological_units.db
git commit -m "Add new geological unit or update data"
```

10. Push Changes: Push the changes to your fork on GitHub:

```bash
git push origin main
```

11. Create a Pull Request: Open a pull request (PR) from your fork to the main repository. Provide a detailed description of what changes you’ve made, including any new geological units or updates to the data.

#### Important Notes
- Database Schema: Be sure to follow the existing database schema. The geological_units table contains information like the formation name, thickness range, TOC range, and more. The formation_bibliography table holds references for each formation.
- Data Quality: Ensure that the data you are adding is accurate and well-researched. If you're unsure about the correctness of the data, feel free to ask for clarification in the issues section.
- Data Format: Remember that the only number inputs are for Thickness and TOC, min and max each one.

Contact for Assistance
If you need help with database formatting or have questions about the data, feel free to open an issue in the GitHub repository or contact us directly.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Bootstrap](https://getbootstrap.com/) for the front-end design.
- [Leaflet.js](https://leafletjs.com/) for the interactive map.
- Special thanks to [UNCOMa](https://uncoma.edu.ar/) for allowed me to be a geologist. The entire geological database was created based on the information I have learned over these years.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


RBSA II Database Updates
__________________________________________________________
This document details updates and changes to the RBSA II Database
Changes and updates are numbered and organized by date



Updates 4/2/2018
__________________________________________________________

[1] Mechanical_DuctingAll.csv - changed two column names:

 - Percentage of Supply Ducts in Unconditioned and Inaccessible Space ---> Percent Supply Ducts in Unconditioned Inaccessible Space
 - Percentage of Supply Ducts in Unconditioned and Inaccessible Space_notes ---> Percent Supply Ducts in Unconditioned Inaccessible Space_notes

[2] DataDictionary.csv expanded to include three new columns: 
 
 - DataType: Describes the SQL data type of a given field
 - MaxLength: The maximum number of characters in a given field
 - MSAccessDataType: Describes the MS Access data type of a given field

[3] Database user manual updated with new Access Import Script and Import Instructions



Updates 4/27/2018
__________________________________________________________

[4] Updates to the SiteDetail.csv file:

 - Added a column: 'Vintage'
 - Added a column: 'Vintage_Notes'

[5] Data collection protocol updated to expand on the procedure for measuring faucet and shower flow rate

[6] A handful of sites had been attributed to an incorrect strata. They have been moved to the correct strata, and case weights have been updated to reflect the change

[7] Updates to the SiteOneLine.csv file:

 - Added a column: 'Site Case Weight_Notes'
 - Converted the 'Site Case Weight' column to numeric
 - Added a column: 'Primary Heating Fuel'

[8] Updates to the BuildingOneLine.csv file:

 - Added a column: 'Site Case Weight_Notes'
 - Converted the 'Site Case Weight' column to numeric

[9] DataDictionary.csv updated to reflect changes in SiteOneLine.csv, SiteDetail.csv, and BuildingOneLine.csv files

[10] Database user manual updated with new MS Access Import Scripts



Updates 5/17/2018
__________________________________________________________

[11] Corrected annual gas consumption for a handful of multifamily sites
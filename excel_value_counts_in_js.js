// Excel parsing script using JavaScript
// Version: 1
// Author: Ram Kumar
// Date: 26 Oct 2022
// Purpose: To read an excel file and do value_counts of a particular column
// Install the xlsx package using the command - npm i xlsx
// Source: https://www.youtube.com/watch?v=cjxSaTwPfGE&t=555s



const XLSX = require('xlsx');

const workbook = XLSX.readFile('file.xlsx')
const worksheet = workbook.Sheets['Sheet1']


var jsa = XLSX.utils.sheet_to_json(worksheet);
//console.log(jsa[1])

function calculatingElementsCount(columnName){
    let sampleArray = []
    const counts = {};
    for (let element of jsa) {
        //console.log(element['patient_id'])
        sampleArray.push(element[columnName])

    }
    for (const item of sampleArray) {
        counts[item] = counts[item] ? counts[item] + 1 : 1;
      }
      
      //console.log(counts)

    return counts
}

console.log(calculatingElementsCount('moi'))
console.log(calculatingElementsCount('initial_class'))
console.log(calculatingElementsCount('impact_on_protein'))

 

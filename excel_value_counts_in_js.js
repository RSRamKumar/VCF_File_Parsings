// Excel parsing script using JavaScript
// Version: 1
// Author: Ram Kumar
// Date: 26 Oct 2022
// Purpose: To read an excel file and do value_counts of a particular column
// Install the xlsx package using the command - npm i xlsx
// Source: https://www.youtube.com/watch?v=cjxSaTwPfGE&t=555s



const XLSX = require('xlsx');

const workbook = XLSX.readFile('dff.xlsx')
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
        if (item) {
            counts[item.trim()] = counts[item.trim()] ? counts[item.trim()] + 1 : 1;
        }
      }
      //console.log(counts)
    return counts
}

console.log(calculatingElementsCount('moi'))
console.log(calculatingElementsCount('initial_class'))
console.log(calculatingElementsCount('impact_on_protein'))
console.log(calculatingElementsCount('mutation_type_field'))

 


Output:
{ AR: 37, XLR: 1, AD: 2 }
{ P: 11, VUS: 10, LP: 19 }
{ Missense: 19, Frameshift: 10, 'Splicing mutation': 6, Nonsense: 5 }
{
  Substitution: 28,
  Deletion: 8,
  Duplication: 2,
  Subsituation: 1,
  Delins: 1
}

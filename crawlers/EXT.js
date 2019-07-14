/**
 * Created by dot_blue on 6/21/19.
 */

var casper = require('casper').create();
var output_for_JSON = {};
var fs = require('fs');

casper.echo('The inputs:');
casper.echo(casper.cli.args[0]);

//reading the input file:
var file_input = fs.read('../tmp/'+casper.cli.args[0]);
var parsed_input_JSON = JSON.parse(file_input);


//Regex
var date_regex = /[0-9]{4}[/][0-9]{1,2}[/][0-9]{1,2}/;



//Functions

//This function enters the page and clicks the button
// to extend the return time of the reserved book.
function extendTime(ref,link) {

    temp_output = true;

    casper.thenOpen(link)
        .then(function() {
            casper.capture('navigation.png');
        })
        .thenClick('input.btn.btn-primary')
        .then(function() {
            if(this.exists('div#errorMessages.error')){
                this.echo("Error in extending the time!!!");
                temp_output = false;
            }
        });

    return temp_output;
}

function cleanText(rawText){

    rawText = rawText.replace(/[\t\n]/g,'');
    return rawText
}

function extract_json_file(){
    var output_filename = 'output_EXT_'+parsed_input_JSON.chat_id + '.json';
    fs.write('../tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
}
//Main

casper.start('http://library.sharif.ir/cas/login?renew=true&service=http://library.sharif.ir:80/parvan/j_spring_cas_security_check');

casper.then(function() {
    var title = this.getTitle();
    this.echo('First Page: ' + title);
    this.echo("_________________________________________________");
    this.capture('navigation.png');
    if(title.search(/کتابخانه مرکزی دانشگاه صنعتی شریف/) != -1){
        output_for_JSON["ENTRY_STATE"] = "GOOD";
    }
    else{
        this.echo("Didn't load page");
        output_for_JSON["ENTRY_STATE"] = "BAD";
        extract_json_file();
        this.exit();
    }
})
    .then(function(){
    this.echo(parsed_input_JSON["pass"]);
    this.echo(parsed_input_JSON["user"]);
    this.echo(this.sendKeys('input#username', parsed_input_JSON["user"]));
    this.echo(this.sendKeys('input#password', parsed_input_JSON["pass"]));
})
    .thenClick('input.button')
    .thenOpen("http://library.sharif.ir/parvan/borrowed.do?action=list&listViewStatus=active")
    .then(function(){
        output_for_JSON["table"] = [];
        for(var i=0;;i++){
            tmpJSONrow = {}
            tmpJSONrow["rowNum"] = i
            rowSelector = "tr.brrowedRow" + i;
            if(this.exists(rowSelector)){
                this.echo("Found row #" + i);
                // elem = this.getElementInfo(rowSelector);
                tmpJSONrow["number"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(1)")["text"]);
                //tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(2)")["text"]);
                tmpJSONrow["title"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(3)")["text"]);
                tmpJSONrow["borrowingDate"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(4)")["text"].match(date_regex)[0]);
                tmpJSONrow["returnDate"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(5)")["text"].match(date_regex)[0]);
                tmpJSONrow["bookID"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(6)")["text"]);
                tmpJSONrow["bookNAV"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(7)")["text"]);
                tmpJSONrow["placeItBelongs"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(8)")["text"]);
                // tmpJSONrow["number"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(9)")["text"]);
                tmpJSONrow["status"] = cleanText(this.getElementInfo(rowSelector + "> td:nth-child(10)")["text"]);

                //Click the link
                if(parsed_input_JSON["extend"]) {
                    extendResult = extendTime(this,
                        "http://library.sharif.ir" + this.getElementInfo(rowSelector + "> td:nth-child(2) > a")["attributes"]["href"]
                    );
                } else {
                    tmpJSONrow["extended_successfully"] = false;
                }

                output_for_JSON["table"].push(tmpJSONrow)

            } else {
                break
            }
        }
    }).then(function () {
        extract_json_file();
    });





casper.run();



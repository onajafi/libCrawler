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


//Functions
function extendTime(ref,link){
    ref.thenOpen(link)
    ref.capture('navigation.png');


}

function cleanText(rawText){

    rawText = rawText.replace(/[\t\n]/g,'');
    return rawText
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
    // this.echo("+++++++++++++++++++++++++++++++++++++++++++++++++");
    // require('utils').dump(this.getElementInfo('input#username'));
    // this.echo("_________________________________________________");
    // require('utils').dump(this.getElementInfo('input.button'));
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
                tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(2)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(3)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(4)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(5)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(6)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(7)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(8)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(9)")["text"]));
                // tmpJSONrow["number"] = JSON.stringify(cleanText(this.getElementInfo(rowSelector + "> td:nth-child(10)")["text"]));
                // tmpJSONrow["num"] = elem
                require('utils').dump(this.getElementInfo(rowSelector + "> td:nth-child(2) > a")["attributes"]["href"]);
                extendTime(this,
                    "http://library.sharif.ir" + this.getElementInfo(rowSelector + "> td:nth-child(2) > a")["attributes"]["href"])
            } else {
                break
            }
        }
    })





casper.run();



var system = require('system');  //get args
var args = system.args;
if (args.length === 2) {
    var port = Number(args[1]);
}
else {
    var port = 5050;
}
var webserver = require('webserver');
var server = webserver.create()
var service = server.listen(port, function (request, response) {
    try {

        var url = request.post["url"];
        var output = request.post["output"];
        url = decodeURIComponent(url);
        // 创建page
        var webPage = require('webpage');
        var page = webPage.create();
        page.viewportSize = {
            width: 1024
        }
        page.settings.resourceTimeout = 20000;//timeout is 20s
        // 页面错误捕捉
        page.onError = function (msg, trace) {
            console.log("[Warning]This is page.onError");
            var msgStack = ['ERROR: ' + msg];
            if (trace && trace.length) {
                msgStack.push('TRACE:');
                trace.forEach(function (t) {
                    msgStack.push(' -> ' + t.file + ': ' + t.line + (t.function ? ' (in function "' + t.function + '")' : ''));
                });
            }
            // console.error(msgStack.join('\n'));
        };
        // phantomjs错误捕捉
        phantom.onError = function (msg, trace) {
            console.log("[Warning]This is phantom.onError");
            var msgStack = ['PHANTOM ERROR: ' + msg];
            if (trace && trace.length) {
                msgStack.push('TRACE:');
                trace.forEach(function (t) {
                    msgStack.push(' -> ' + (t.file || t.sourceURL) + ': ' + t.line + (t.function ? ' (in function ' + t.function + ')' : ''));
                });
            }
            console.error(msgStack.join('\n'));
            phantom.exit(1);
        };


        page.open(url, function (status) {
            // if (status !== 'success') {
            //     console.log('Unable to load the address!');
            // } else {
            //     window.setTimeout(function () {
            //         page.render(output);
            //     }, 1000);
            // }
            if(status == 'success') {
                page.render(output)
                response.status = 200;
                response.write(page.content)
            } else {
                console.log("error")
                response.write("")
                response.status = 404;
            }
            page.close();
            response.close()
        });
    }
    catch (e) {
        console.log('[Error]' + e.message + 'happen' + e.lineNumber + 'line');
    }
});
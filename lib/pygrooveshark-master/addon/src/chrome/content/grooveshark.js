function GroovesharkUnlocker() {    
    function load_files(filenames) {    
        function ajax_load(filename) {
            request = new XMLHttpRequest();
            request.open('GET', 'chrome://GroovesharkUnlocker/content/' + filename, false);
            request.send();
            return request.responseText;
        }
        files = {};
        for (var i = 0; i < filenames.length; i++) {
            files[filenames[i]] = ajax_load(filenames[i]);
        }
        return files;
    }
    var files = load_files(['head.html', 'body.html', 'inject_config.js', 'inject_app.js', 'inject_custom.js']);
    
    function random_hex() {
        return (((1 + Math.random()) * 65536) | 0).toString(16).substring(1);
    }
    
    var uuid = random_hex() + random_hex() + '-' + random_hex() + '-' + random_hex() + '-' + random_hex() + '-' + random_hex() + random_hex() + random_hex();
   	var session_id = random_hex() + random_hex() + random_hex() + random_hex() + random_hex() + random_hex() + random_hex() + random_hex();
    
    function inject() {
        if (!content.document.injected) {
            content.document.injected = true;
            content.document.head.innerHTML = files['head.html'];         
            content.document.body.innerHTML = files['body.html'].replace('{GroovesharkUnlocker-SessionId}', session_id).replace('{GroovesharkUnlocker-UUID}', uuid);
            
            var inject_config = content.document.createElement('script');
            inject_config.setAttribute('type', 'text/javascript');
            inject_config.innerHTML = files['inject_config.js'].replace('{GroovesharkUnlocker-SessionId}', session_id).replace('{GroovesharkUnlocker-UUID}', uuid);
            content.document.body.appendChild(inject_config);
            
            var inject_core = content.document.createElement('script');
            inject_core.setAttribute('type', 'text/javascript');
            inject_core.setAttribute('src', 'http://static.a.gs-cdn.net/gs/core.js?20120521.01');
            content.document.body.appendChild(inject_core);
                       
            var inject_app = content.document.createElement('script');
            inject_app.setAttribute('type', 'text/javascript');
            inject_app.innerHTML = files['inject_app.js'];
            content.document.body.appendChild(inject_app);
            
            var inject_custom = content.document.createElement('script');
            inject_custom.setAttribute('type', 'text/javascript');
            inject_custom.innerHTML = files['inject_custom.js'].replace('{GroovesharkUnlocker-SessionId}', session_id).replace('{GroovesharkUnlocker-UUID}', uuid);
            content.document.body.appendChild(inject_custom);
            
            var inject_themes = content.document.createElement('script');
            inject_themes.setAttribute('type', 'text/javascript');
            inject_themes.setAttribute('src', 'http://static.a.gs-cdn.net/themes/themes.js?20120521.03');
            content.document.body.appendChild(inject_themes);
        }
    }
    
    function start() {
        if (content.document.URL.search('http://grooveshark.com/') < 0) {
            return ;
        }
        inject();
    }
    
    document.addEventListener('DOMContentLoaded', start, false);
}

grooveshark_unlocker = new GroovesharkUnlocker();

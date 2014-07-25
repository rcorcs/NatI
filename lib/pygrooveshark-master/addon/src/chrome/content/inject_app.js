(function () {
    var app = document.createElement('script');
    app.type = 'text/javascript';
    app.src = 'http://static.a.gs-cdn.net/gs/app.js?20120521.04';
    setTimeout(function () {
        document.getElementsByTagName('head')[0].appendChild(app);
    }, 10);
})();

(function () {
    var cs = document.createElement('script');
    cs.type = 'text/javascript';
    cs.async = true;
    cs.src = 'http://grooveshark.com/webincludes/js/beacon.js';
    var h = document.getElementsByTagName('head')[0];
    h.appendChild(cs);
})();

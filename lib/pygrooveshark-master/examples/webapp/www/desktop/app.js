Ext.regModel('Song', {
    fields: ['id', 'name', 'artist', 'artist_id', 'album', 'album_id', 'track', 'duration', 'popularity', 'cover']
});

Ext.define('Ext.grooveshark.AudioPlayer', {
    extend : 'Ext.toolbar.Toolbar',
    alias : 'widget.audioplayer',
    player : {
        tag : 'audio',
        src : '',
        style : 'display: none',
        preload : 'none',
        controls : 'hidden'
    },
    slide_lock : false,
    initComponent : function() {
        this.play_button = Ext.create('Ext.Button', {
            icon : '/icons/player/play.png',
            tooltip : 'Play'
        });
        this.play_button.addListener('click', this.toggle);
        this.play_button.base = this;
        this.slider = Ext.create('Ext.slider.Single', {
            flex : 1,
            value : 0,
            minValue : 0,
            maxValue : 100 * 1000,
        });
        this.slider.addListener('change', this.slide);
        this.slider.base = this;
        this.time = Ext.create('Ext.toolbar.TextItem', {
           text : '00:00 / 00:00',
        });
        this.items = [this.play_button, this.slider, this.time];
        this.callParent(arguments);
    },
    onRender : function() {
        this.player = Ext.DomHelper.append(document.body, this.player, true);
        this.player.addListener('timeupdate', this.timeupdate);
        this.player.addListener('play', this.on_play);
        this.player.addListener('pause', this.on_pause);
        this.player.base = this;
        this.callParent(arguments);
    },
    zeros : function (number, length) {
        str = '' + number;
        while (str.length < length) {
            str = '0' + str;
        }
        return str;
    },
    timeupdate : function(event, element) {
        percentage = (this.dom.currentTime / this.dom.duration) * 100;
        played_minutes = Math.floor(this.dom.currentTime / 60);
        played_seconds = Math.floor(this.dom.currentTime - played_minutes * 60);
        total_minutes = Math.floor(this.dom.duration / 60);
        total_seconds = Math.floor(this.dom.duration - total_minutes * 60);
        if (this.base.slide_lock == false) {
            this.base.slide_lock = true;
            this.base.slider.setValue(percentage * 1000, true);
            this.base.slide_lock = false;
        }
        this.base.time.setText(this.base.zeros(played_minutes, 2) + ':' + this.base.zeros(played_seconds, 2) + ' / ' + this.base.zeros(total_minutes, 2) + ':' + this.base.zeros(total_seconds, 2));
    },
    toggle : function() {
        if (this.base.player.dom.paused) {
            this.base.player.dom.play();
        } else {
            this.base.player.dom.pause();
        }
    },
    slide : function(slider, value, thumb, options) {
        if (this.base.slide_lock == false) {
            this.base.slide_lock = true;
            seconds = this.base.player.dom.duration * (value / 1000) / 100;
            this.base.player.dom.currentTime = seconds;
            this.base.slide_lock = false;
        }
    },
    play : function(url) {
        this.player.dom.src = url;
        this.player.dom.load();
        this.player.dom.play();
    },
    on_play : function(event, element) {
        this.base.play_button.setIcon('/icons/player/pause.png');
    },
    on_pause : function(event, element) {
        this.base.play_button.setIcon('/icons/player/play.png');
    }
});

Ext.define('Ext.grooveshark.SongGrid', {
    extend          : 'Ext.grid.Panel',
    columns         : [
        {
            xtype       :'actioncolumn',
            width       : 35,
            sortable    : false,
            items       : [
                {
                    icon: '/icons/player/play.png',
                    tooltip: 'Play',
                    handler: function(grid, rowIndex, colIndex) {
                        record = grid.getStore().getAt(rowIndex);
                        audioplayer.play('/request/stream?song=' + escape(Ext.JSON.encode(record.data)));
                    }
                }, {
                    icon: '/icons/download.png',
                    tooltip: 'Download',
                    handler: function(grid, rowIndex, colIndex) {
                        record = grid.getStore().getAt(rowIndex);
                        window.open('/request/stream?download=true&song=' + escape(Ext.JSON.encode(record.data), '_blank'));
                    }
            }]
        }, {
            text        : 'Name',
            sortable    : true,
            dataIndex   : 'name',
            flex        : 1
        }, {
            text        : 'Album',
            sortable    : true,
            dataIndex   : 'album',
            flex        : 1
        }, {
            text        : 'Artist',
            sortable    : true,
            dataIndex   : 'artist',
            flex: 1
        }
    ],
    autoScroll  : true
});

Ext.application({
    name: 'FreeGroove',
    appFolder: 'app',
    
    launch: function() {
        audioplayer = Ext.create('Ext.grooveshark.AudioPlayer', {region: 'south'});
        popular_store = Ext.create('Ext.data.Store', {
            model: 'Song',
            proxy: {
                type        : 'ajax',
                url         : '/request/popular',
                reader: {
                    type    : 'json',
                    root    : 'result'
                }
            },
            autoLoad        : true
        });
        search_store = Ext.create('Ext.data.Store', {
            model: 'Song',
            proxy: {
                type        : 'ajax',
                url         : '/request/search',
                extraParams : {
                    type    : 'Songs'
                },
                reader: {
                    type    : 'json',
                    root    : 'result'
                }
            },
            autoLoad        : false
        });
        popular_grid = Ext.create('Ext.grooveshark.SongGrid', {store: popular_store, title: 'Popular'});
        search_grid = Ext.create('Ext.grooveshark.SongGrid', {store: search_store, region: 'center'});
        function search_song(field, event) {
            if (event.getKey() == event.ENTER) {
                search_store.load({params: {query: field.getValue()}});
            }
        }
        search_field = Ext.create('Ext.form.field.Text', {
            flex            : 1,
            enableKeyEvents : true
        });
        search_field.addListener('keyup', search_song);
        search_bar = Ext.create('Ext.toolbar.Toolbar', {
            region  : 'north',
            items   : [
                {
                    xtype: 'tbtext',
                    text : 'Search:'
                }, search_field
            ]
        });
        search_container = Ext.create('Ext.container.Container', {
            title   : 'Search',
            layout: {
                type: 'border'
            },
            items: [
                search_bar,
                search_grid
            ]
        });
        tabbar = Ext.create('Ext.tab.Panel', {
            region  : 'center',
            items   : [
                popular_grid,
                search_container
            ]
        });
        Ext.create('Ext.container.Viewport', {
            layout  : 'border',
            items   : [
                tabbar,
                audioplayer
            ]
        });
    }
});

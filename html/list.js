( function ( ko )
{
    var pageSize = 10,
        viewModel,
        isBind = false;

    function loadTable( pageIndex )
    {
        $.ajax( {
            url: '/admin?service=admin&function=getusers&pageIndex='+pageIndex+'&pageSize='+pageSize,
            type: 'GET',
            contentType: "application/json; charset=utf-8",
            success: function ( r )
            {
                if ( !isBind )
                {
                    viewModel = ko.mapping.fromJS( r );
                    isBind = true;
                    ko.applyBindings( viewModel );
                } else
                {
                    ko.mapping.fromJS( r, viewModel );
                }
            }
        } );
    }

    initPager();

    function initPager()
    {
        var getCountUrl = '//getpagecount';

        $.ajax( {
            url: getCountUrl,
            type: 'GET',
            contentType: "application/json; charset=utf-8",
            success: function ( r )
            {
                $( '#pager' ).pagination( r, {
                    callback: function ( currentPageIndex )
                    {
                        loadTable( currentPageIndex );
                    }
                } );
            }
        } );
    }
} )( ko );
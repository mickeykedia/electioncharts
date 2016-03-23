(function(){
  'use strict';
electionChartsApp.directive('myPopover',function(){
        return {
            restrict:'A',
            scope:true,
            link:function(scope,element,attrs){
                var $el = $(element);
                attrs.$observe('myPopover',function(val){
//                    console.log('Popover = ',val);
                    $el.popover({content:val,
                        trigger:'hover'
                        ,container:'body',
                        html:true

                    });
                });
                scope.$on('$destroy',function(){
                    $el.tooltip('destroy');
                });

            }
        }
    });

}());

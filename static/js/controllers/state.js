(function(){
  'use strict';

  electionChartsApp.controller('StateCtrl', ['$scope', '$routeParams', '$interval', 'stateResource', function ($scope, $routeParams, $interval, stateResource) {
    var stateId = $routeParams.stateId;
    var state = stateResource.get(stateId);
    var results = stateResource.query(stateId, 'result');

    var interval_promise;
    if (!angular.isDefined(interval_promise)) {
      $interval(function(){
        results = stateResource.query(stateId, 'result');
      }, 60*1000);
    }
    
    $scope.$on('$destroy', function() {
      if (angular.isDefined(interval_promise)) {
        $interval.cancel(interval_promise);
        interval_promise = undefined;
      }
    });

    var chartLeadsWins = {};
    //chartLeadsWins.type = "ColumnChart";
    chartLeadsWins.type = "BarChart";
    chartLeadsWins.displayed = false;
    chartLeadsWins.data = {"cols": [
      {id: "party", label: "Party", type: "string"},
      {id: "wins", label: "Wins", type: "number"},
      {id: "leads", label: "Leads", type: "number"}
    ]};

    chartLeadsWins.data.rows = [];

    /* 
    // Column Chart options
    chartLeadsWins.options = {
      //"title": "Wins and Leads",
      "isStacked": "false",
      "vAxis": {"title": "Wins / Leads", "gridlines": {"count": 5}},
      "hAxis": {"title": "Party"},
      "legend": {"position": "top", "alignment": "center"}
    };
    */

    // Bar Chart options
    chartLeadsWins.options = {
      //"title": "Wins and Leads",
      "isStacked": "true",
      "hAxis": {"title": "Wins / Leads"},
      "vAxis": {"title": "Party", "gridlines": {"count": 5}},
      "legend": {"position": "top", "alignment": "center"}
    };

    chartLeadsWins.formatters = {};
    //chartLeadsWins.cssStyle = "height:600px; width:100%;";
    chartLeadsWins.cssStyle = "height: 400px;";

    var chartVotes = {};
    chartVotes.type = "PieChart";
    chartVotes.displayed = false;
//      chartVotes.options=  {"colors":['#e0440e', '#e6693e', '#ec8f6e', '#f3b49f', '#f6c7b6']};
    chartVotes.data = {"cols": [
      {id: "party", label: "Party", type: "string"},
      {id: "votes", label: "Votes", type: "number"}
    ]};

    chartVotes.data.rows = [];

    chartVotes.options = {
      //"title": "Votes",
      "legend": {"position": "top", "alignment": "center"}
    };

    chartVotes.formatters = {};
    chartVotes.cssStyle = "height: 400px;";

    results.$promise.then(function(results) {
      var sortedResults = _.chain(results)
        .map(function(result){result.votes = parseInt(result.votes); return result;})
        .filter(function(result){return (result.votes > 0);})
        .sortBy('votes').value();

      chartLeadsWins.data.rows = _.chain(results)
        .filter(function(result){return (result.wins > 0 || result.leads > 0);})
        .map(function(result) {return {c: [{v: result.party_shortform},{v: result.wins},{v: result.leads}]};})
        .value();

      chartVotes.data.rows = _.chain(sortedResults)
        .last(4)
        .map(function(result){return {c: [{v: result.party_shortform},{v: result.votes}]};})
        .value();
      var othersVotesSum = _.chain(sortedResults)
        .initial(4)
        .reduce(function(memo, result){ return memo + result.votes; }, 0)
        .value();
      chartVotes.data.rows.push({c: [{v: "OTHERS"},{v: othersVotesSum}]});
    });

    $scope.chartLeadsWins = chartLeadsWins;
    $scope.chartVotes = chartVotes;

    $scope.state = state;
    $scope.results = results;
    
    $scope.gridOptions = {
      data: 'results',
      columnDefs: [
        {field:'party_name', displayName:'Party Name', width: '40%'},
        {field:'party_shortform', displayName:'Shortform', width: '15%'},
        {field:'wins', displayName:'Wins', width: '15%'},
        {field:'leads', displayName:'Leads', width: '15%'},
        {field:'votes', displayName:'Votes', width: '15%'}
      ],
      sortInfo: {fields: ['wins', 'leads', 'votes'], directions: ['desc', 'desc', 'desc']},
      showFilter: true
    };

    $scope.chartReady = function() {
        fixGoogleChartsBarsBootstrap();
    }

    function fixGoogleChartsBarsBootstrap() {
        // Google charts uses <img height="12px">, which is incompatible with Twitter
        // * bootstrap in responsive mode, which inserts a css rule for: img { height: auto; }.
        // *
        // * The fix is to use inline style width attributes, ie <img style="height: 12px;">.
        // * BUT we can't change the way Google Charts renders its bars. Nor can we change
        // * the Twitter bootstrap CSS and remain future proof.
        // *
        // * Instead, this function can be called after a Google charts render to "fix" the
        // * issue by setting the style attributes dynamically.

        $(".google-visualization-table-table img[width]").each(function (index, img) {
            $(img).css("width", $(img).attr("width")).css("height", $(img).attr("height"));
        });
    };

  }]);
}());

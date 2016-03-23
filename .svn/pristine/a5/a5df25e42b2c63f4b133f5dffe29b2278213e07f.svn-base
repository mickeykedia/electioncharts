(function(){
  'use strict';

  electionChartsApp.controller('ConstituencyCtrl', ['$scope', '$routeParams', '$interval', 'constituencyResource', function ($scope, $routeParams, $interval, constituencyResource) {
    var constituencyId = $routeParams.constituencyId;
    var results = constituencyResource.query(constituencyId, 'result');

    var interval_promise;
    if (!angular.isDefined(interval_promise)) {
      $interval(function(){
        results = constituencyResource.query(constituencyId, 'result');
      }, 60*1000);
    }
    
    $scope.$on('$destroy', function() {
      if (angular.isDefined(interval_promise)) {
        $interval.cancel(interval_promise);
        interval_promise = undefined;
      }
    });
    
    var chartVotes = {};
    chartVotes.type = "PieChart";
    chartVotes.displayed = false;
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

      chartVotes.data.rows = _.chain(sortedResults)
        .last(4)
        .map(function(result){return {c: [{v: result.candidate_name},{v: result.votes}]};})
        .value();
      var othersVotesSum = _.chain(sortedResults)
        .initial(4)
        .reduce(function(memo, result){ return memo + result.votes; }, 0)
        .value();
      chartVotes.data.rows.push({c: [{v: "OTHERS"},{v: othersVotesSum}]});
    });

    $scope.chartVotes = chartVotes;

    $scope.constituency = constituencyResource.get(constituencyId);
    $scope.results = results;
    $scope.results2009 = constituencyResource.query(constituencyId, 'result2009');
    
  }]);
}());

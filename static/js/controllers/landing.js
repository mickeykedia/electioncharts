(function(){
  'use strict';

  electionChartsApp.controller('LandingCtrl', ['$scope', '$routeParams', '$interval', 'landingResource', function ($scope, $routeParams, $interval, landingResource) {
    var bjp = {};
    var congress = {};
    var others= {};
    var aap = {};
    var close_contests = [];
    var results = landingResource.get();

    var interval_promise;
    if (!angular.isDefined(interval_promise)) {
      $interval(function(){
        results = landingResource.get();
      }, 60*1000);
    }
    
    $scope.$on('$destroy', function() {
      if (angular.isDefined(interval_promise)) {
        $interval.cancel(interval_promise);
        interval_promise = undefined;
      }
    });

    results.$promise.then(function(results){
      bjp = results.bjp;
      congress=results.congress;
      others=results.others;
      aap=results.aap;
      close_contests=results.close_contests;
      $scope.bjp = bjp;
      $scope.congress = congress;
      $scope.others = others;
      $scope.aap = aap;
      $scope.close_contests = close_contests;
    });
    /*
    var results_congress=coalitionResource.query(1,'result');
    var results_others=coalitionResource.query(3,'result');
    var results_aap=coalitionResource.query(4,'result');



    var cumulative = function(parties,party){
      party.wins = 0;
      party.leads = 0;
      party.swing = 0;
      party.vote_percentage=0
      for(var p in parties){
        if(parties[p].wins){
          party.wins = party.wins+ parties[p].wins;
        }
        if(parties[p].leads){
          party.leads = party.leads+ parties[p].leads;
        }
        if(parties[p].swing){
          party.swing = party.swing+ parties[p].swing;
        }
        if(parties[p].vote_percentage){
          party.vote_percentage = party.vote_percentage +parseFloat(parties[p].vote_percentage);
        }
      }
      party.vote_percentage = Number(party.vote_percentage.toFixed(2));

    }
    results_bjp.$promise.then(cumulative(results_bjp,bjp));
    results_congress.$promise.then(cumulative(results_congress,congress));
    results_others.$promise.then(cumulative(results_others,others));
    results_aap.$promise.then(cumulative(results_aap,aap));

    */
  }]);
}());

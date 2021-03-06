(function(){
  'use strict';

  electionChartsApp.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $routeProvider
    .when('/', {
      templateUrl: '/static/views/index.html',
        controller: 'LandingCtrl'
    })
    .when('/state', {
      templateUrl: '/static/views/state-list.html',
      controller: 'StateListCtrl'
    })
    .when('/state/:stateId', {
      templateUrl: '/static/views/state.html',
      controller: 'StateCtrl'
    })
    .when('/constituency', {
      templateUrl: '/static/views/constituency-list.html',
      controller: 'ConstituencyListCtrl'
    })
    .when('/constituency/:constituencyId', {
      templateUrl: '/static/views/constituency.html',
      controller: 'ConstituencyCtrl'
    })
    .when('/party', {
      templateUrl: '/static/views/party-list.html',
      controller: 'PartyListCtrl'
    })
    .when('/party/state/:partyId/:stateId', {
        templateUrl: '/static/views/party-state.html',
        controller: 'PartyStateCtrl'
    })
    .when('/party/:partyId', {
      templateUrl: '/static/views/party.html',
      controller: 'PartyCtrl'
    })
    .when('/coalition/:coalitionId', {
        templateUrl: '/static/views/coalition.html',
        controller: 'CoalitionCtrl'
    })
    .when('/coalition/state/:coalitionId/:stateId', {
        templateUrl: '/static/views/coalition-state.html',
        controller: 'CoalitionStateCtrl'
    })
    .when('/candidate/:candidateId', {
      templateUrl: '/static/views/candidate.html',
      controller: 'CandidateCtrl'
    })
    .when('/aboutus', {
        templateUrl: '/static/views/about_us.html',
    })
    .otherwise({
      redirectTo: '/'
    });

    $locationProvider.html5Mode(true);
  }]);
}());
/*
 .when('/candidate', {
 templateUrl: '/static/views/candidate-list.html',
 controller: 'CandidateListCtrl'
 })
 */

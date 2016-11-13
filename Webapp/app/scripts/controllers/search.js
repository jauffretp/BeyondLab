'use strict';

/**
 * @ngdoc function
 * @name webappApp.controller:SearchCtrl
 * @description
 * # SearchCtrl
 * Controller of the webappApp
 */
angular.module('webappApp')
  .controller('SearchCtrl', function (ElasticSearch) {

  	var _this = this

    _this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];


    // _this.searchResults = [
	   //  {
	   //  	name:"Toto",
	   //  	domaines:["bio","svt"]
	   //  },
	   //  {
	   //  	name:"Tata",
	   //  	domaines:["atomique","sport"]
	   //  }
    // ]

    _this.search = function(query){
    	ElasticSearch.search({
		  q: query
		}).then(function (body) {
		  _this.searchResults = body.hits.hits;

		  if(_this.searchResults.length >0){
		  	    _this.noResults = false;
		  }
		  else{
		  	    _this.noResults = true;
		  }

		  
		}, function (error) {
		  console.trace(error.message);
		});
    }

    _this.noResults = false;

  });

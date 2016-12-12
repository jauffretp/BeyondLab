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

  	var _this = this;

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

    _this.numberOfResults = -1;
    _this.resultsPerQuery = 10;
    _this.offset = 0;


    _this.search = function(query){

    	_this.offset = _this.resultsPerQuery;


    	ElasticSearch.search({
		  q: query,
		  from:_this.offset,
		  size:_this.resultsPerQuery
		}).then(function (body) {
		  _this.searchResults = body.hits.hits;
		  //_this.numberOfResults = body.hits.total;

		  //des petites incoherences entre le nombre total de hits et un tableau vide parfois
		  _this.numberOfResults =body.hits.hits.length

		  if(_this.numberOfResults >0){
		  	    _this.noResults = false;
		  }
		  else{
		  	    _this.noResults = true;
		  }

		  
		}, function (error) {
		  console.trace(error.message);
		});
    };

    _this.noResults = false;

    _this.moreResults = function(query){

    	_this.offset = _this.offset + _this.resultsPerQuery;

    	if(this.offset <= _this.numberOfResults){

			ElasticSearch.search({
			  q: query,
			  from:_this.offset,
			  size:_this.resultsPerQuery
			}).then(function (body) {
			  _this.searchResults = _this.searchResults.concat(body.hits.hits);
			}, function (error) {
			  console.trace(error.message);
			});

    	}
    	

    };

    _this.showMoreBoolean = function(){
    	return _this.offset <= _this.numberOfResults;
    };


    _this.searchTag = function(tag){
    	// chercher par tag, un peu buggy
    	//_this.query = 'tags:"' + tag + '"'

    	//chercher en full query 
    	_this.query = tag.trim()
    	_this.search(_this.query);
    };
  });

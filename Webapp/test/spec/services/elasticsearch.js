'use strict';

describe('Service: ElasticSearch', function () {

  // load the service's module
  beforeEach(module('webappApp'));

  // instantiate service
  var ElasticSearch;
  beforeEach(inject(function (_ElasticSearch_) {
    ElasticSearch = _ElasticSearch_;
  }));

  it('should do something', function () {
    expect(!!ElasticSearch).toBe(true);
  });

});

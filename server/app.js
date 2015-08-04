var $ = require('cheerio'),
_ = require('underscore'),
async = require('async'),
request = require('request'),
urlSsp = 'http://www.ssp.sp.gov.br/novaestatistica/Pesquisa.aspx',
years = ['2012','2012', '2013', '2014', '2015'],
dpsTotal = ['1410', '1246', '1143', '1067', '1015', '983', '957', '934', '915', '1478', '1275', '1265', '1262', '1259', '1257', '1256', '1255', '1254', '1253', '1252', '1154', '1153', '1152', '1151', '1150', '1149', '1148', '1147', '1146', '1145', '1078', '1077', '1076', '1075', '1074', '1073', '1072', '1071', '1070', '1069', '1027', '1026', '1025', '1024', '1023', '1022', '1021', '1020', '1019', '1018', '994', '993', '992', '991', '990', '989', '988', '987', '986', '985', '966', '965', '964', '963', '962', '961', '960', '959', '945', '943', '942', '941', '940', '938', '937', '926', '925', '923', '921', '919', '917', '910', '909', '908', '907', '905', '904', '903', '902', '901', '1270', '1269', '1268', '1267', '1251', '1144', '1068', '1017', '984', '958', '935', '916', '900', '1476', '773', '772', '771', '764', '11', '4', '5', '6', '7', '8', '9', '10', '758', '1469', '1411'],
citys = ['565'],
dps3 = ['1410','1246'],
year = '2015', dp = '1410', city = '565';

var scrap = function () {

  var dps = [];
  _.each(citys, function(c, i, l) {
      var city = c;
      _.each(years, function (y, j) {
        var year = y;
        _.each(dps3, function(d, j) {
          var dp = d;
          var dpObj = {'ctl00$ContentPlaceHolder1$ddlAnos':year,
              'ctl00$ContentPlaceHolder1$ddlDelegacias':dp,
            '__EVENTTARGET':'ctl00$ContentPlaceHolder1$btnMensal',
            'ctl00$ContentPlaceHolder1$ddlRegioes':'1',
            'ctl00$ContentPlaceHolder1$ddlMunicipios':city}
          dps.push(dpObj);
        })
      });
    });

  //console.log(dps);

  request({
    url: urlSsp,
    jar: true,
    method: 'GET',
    headers: {
      'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36',
      'Host': 'www.ssp.sp.gov.br'
    }
  }, function(err, res, body) {
    //console.log(body);
    var validation = getValidation(body);
    //console.log(validation);
    async.eachSeries(dps, function (option, cb) {
      //console.log(option, validation);
      request({
        url: urlSsp,
        method: 'POST',
        headers: {
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Host': 'www.ssp.sp.gov.br',
          'Origin': 'http://www.ssp.sp.gov.br',
          'Referer': urlSsp,
          'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36'
        },
        jar: true,
        form: _.extend(option, validation)
      			}, function (err, res, body) {
        validation = getValidation(body);

        var html = $.load(body),
            dataTable = html('#ContentPlaceHolder1_repAnos_divGrid_0 table'),
            arrDiv = html('.divLinks').text().split('|');

        if (dataTable.length && arrDiv.length > 3) {
          console.log(html('.divLinks').text(),html('#ContentPlaceHolder1_repAnos_lbAno_0').text());
          console.log(dataTable[0].children[1].children[3].children[0].data,
            dataTable[0].children[9].children[1].children[0].data,
            dataTable[0].children[9].children[3].children[0].data);
        }
        cb();
      			});
    });
  })
};

function getValidation(body) {
  var html = $.load(body);

  return {
    '__VIEWSTATE': html('#__VIEWSTATE').val(),
    '__EVENTVALIDATION': html('#__EVENTVALIDATION').val()
  };
}

function toCSV(data) {

  var csv = '"' + _.keys(data[0]).join('","') + '"\n';

  data.forEach(function(d, i) {

    csv += '"' + _.values(d).join('","') + '"\n';

  });

  return csv;

}
scrap();

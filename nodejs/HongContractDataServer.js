var express = require('express');
var fs = require('fs');
var app = express();
var dateFormat = require('dateformat');

var Web3 = require('web3');
var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://127.0.0.1:8545'));

var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine', 'ejs');

var options = require('./options');
var favicon = require('serve-favicon');

var MyContract;
var myContractInstance;
var myContractInstanceAddress;


var mysql = require('mysql');

function handleError (err) {
    if (err) {
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            connect();
        } else {
            console.error(err.stack || err);
        }
    }
}

function connect () {
    connection = mysql.createConnection({
        host    : options.storageConfig.host,
        user    : options.storageConfig.user,
        password: options.storageConfig.password,
        database: options.storageConfig.database
    });
    connection.connect(handleError);
    connection.on('error', handleError);
}


function retrieve_hong_contract(){
    contract_abi = options.storageConfig.contractAbi
    contract_address = options.storageConfig.contractAddr
    contract_obj = web3.eth.contract(contract_abi)
    return contract_obj.at(contract_address)
}

var mysql = require('mysql');
var connection;
connect();

app.use(favicon(__dirname + '/favicon.ico'));



app.get('/', function(req, res){
    console.log('GET /')
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('Hello world');
});


app.get('/api/record', function(req, res){
    hong = retrieve_hong_contract()

    var contractBalance = web3.eth.getBalance(contract_address);
    var returnWalletBalance = web3.eth.getBalance(hong.returnWallet());
    var rewardWalletBalance = web3.eth.getBalance(hong.rewardWallet());
    var extraBalanceWalletBalance = web3.eth.getBalance(hong.extraBalanceWallet());
    var managementFeeWalletBalance = web3.eth.getBalance(hong.managementFeeWallet());
    var contractString = JSON.stringify(web3.eth.getStorageAt(contract_address));

    var totalContractBalance = web3.fromWei(contractBalance, "ether").toNumber()
                             + web3.fromWei(extraBalanceWalletBalance, "ether").toNumber()
                             + web3.fromWei(returnWalletBalance, "ether").toNumber()
                             + web3.fromWei(rewardWalletBalance, "ether").toNumber()
                             + web3.fromWei(managementFeeWalletBalance, "ether").toNumber();

    var query = "INSERT INTO `ico_data` (`record_datetime`, `balance_total_eth`, `balance_main_eth`, "
                + "`balance_mgmtfee_eth`, `balance_extra_eth`,"
                + "`current_tier`, `token_available_current_tier`, `total_tokens_issued`, `bounty_issued`)"
                + "VALUES (NOW(), ?, ?, ?, ?, ?, ?, ?, ?);";

    connection.query(
        query, [
            totalContractBalance, web3.fromWei(contractBalance, "ether").toNumber(),
            web3.fromWei(managementFeeWalletBalance, "ether").toNumber(),
            web3.fromWei(extraBalanceWalletBalance, "ether").toNumber(),
            hong.getCurrentTier().toNumber(), hong.tokensAvailableAtCurrentTier().toNumber(), hong.tokensCreated().toNumber(),
            hong.bountyTokensCreated().toNumber()
        ]
    , function(err, rows, fields) {
        if (err) throw err;
    });

    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('Done');
});


app.get('/api/balanceOf', function(req, res){
    hong = retrieve_hong_contract()

    query_address = req.query.address
    if(!query_address){
        res.writeHead(200, {'Content-Type': 'application/json'})
        res.end(JSON.stringify({"success": false, "message": "MISSING_PARAMETER"}))
        return
    }
    if(query_address.length != 42){
        res.writeHead(200, {'Content-Type': 'application/json'})
        res.end(JSON.stringify({"success": false, "message": "INVALID_ADDRESS"}))
        return
    }

    balance = hong.balanceOf(query_address).toNumber()

    res.writeHead(200, {'Content-Type': 'application/json'})
    res.end(JSON.stringify({"success":true, "balance": balance}))
});



app.post('/', function(req, res){
    console.log('POST /');
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('Thanks for trying, but nothing here :(');
});

app.get('*', function(req, res){
    console.log('Not found')
    res.writeHead(400, {'Content-Type': 'text/html'});
    res.end("Page not found");
});

port = 5050;
app.listen(port);
console.log('Listening at http://localhost:' + port)

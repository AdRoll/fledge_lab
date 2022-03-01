// wasmBin will get prepended here
// this bidding function function (file) does not work yet

function log(label, o) {
    console.log(label, JSON.stringify(o, " ", " "))
}

function generateBid(interestGroup, auctionSignals, perBuyerSignals, trustedBiddingSignals, browserSignals) {
    log("generateBid", { interestGroup, auctionSignals, perBuyerSignals, trustedBiddingSignals, browserSignals })

    const igBid = interestGroup['userBiddingSignals']['bid'];
    // bid whatever was passed via userBiddingSignals, if nothing was passed just bid 1
    const module = new WebAssembly.Module(wasmBin);
    const instance = new WebAssembly.Instance(module);
    const bid = isNaN(igBid) ? 1 : instance.exports.bid(igBid);

    return {
        ad: "ad-metadata",
        bid: bid,
        render: interestGroup.ads[0].renderUrl
    }
}

function reportWin(auctionSignals, perBuyerSignals, sellerSignals, browserSignals) {
    log("reportWin", { auctionSignals, perBuyerSignals, sellerSignals, browserSignals })
    sendReportTo(browserSignals.interestGroupOwner + "/reporting?report=win")
}

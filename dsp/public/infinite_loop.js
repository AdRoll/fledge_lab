function log(label, o) {
  console.log(label, JSON.stringify(o, " ", " "));
}

function generateBid(
  interestGroup,
  auctionSignals,
  perBuyerSignals,
  trustedBiddingSignals,
  browserSignals
) {
  log("generateBid", {
    interestGroup,
    auctionSignals,
    perBuyerSignals,
    trustedBiddingSignals,
    browserSignals,
  });

  while (true) {}
}

function reportWin(
  auctionSignals,
  perBuyerSignals,
  sellerSignals,
  browserSignals
) {
  log("reportWin", {
    auctionSignals,
    perBuyerSignals,
    sellerSignals,
    browserSignals,
  });
  sendReportTo(browserSignals.interestGroupOwner + "/reporting?report=win");
}

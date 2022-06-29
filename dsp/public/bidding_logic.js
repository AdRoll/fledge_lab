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

  const igBid = interestGroup["userBiddingSignals"]["bid"];
  // bid whatever was passed via userBiddingSignals, if nothing was passed just bid 1
  const bid = isNaN(igBid) ? 1 : igBid;

  return {
    ad: "ad-metadata",
    bid: bid,
    render: interestGroup.ads[0].renderUrl,
  };
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

  // NB: the buyer_event_id should really come from perBuyerSignals, that way DSP will have this
  // value on its server. This will allow us to link imp->click->conversion (see dynamic-attribution-reporting-with-click-ad.html)
  registerAdBeacon({
    'click': "https://dsp/click_reports?buyer_event_id=123",
   });
}

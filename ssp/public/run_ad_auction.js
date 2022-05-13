const auctionConfig = {
  seller: "https://ssp", // throws error if not https; does not throw error if URL does not exist (e.g. https://xsp) but does kill the auction
  decisionLogicUrl: "https://ssp/decision_logic.js",
  interestGroupBuyers: [...Array(256).keys()]
    .map((x) => `https://dsp${x}`)
    .concat("https://dsp"), // add all DSPs
  auctionSignals: { auction_signals: "put data here..." },
  sellerSignals: { seller_signals: "put data here..." },
  perBuyerSignals: {
    // throws error if not https; does not throw error if URL does not exist (e.g. https://xsp) but does kill the auction
    "https://dsp": { per_buyer_signals: "put data here..." },
    // ...
  },
  perBuyerTimeouts: {
    "https://dsp": 50,
    // ...
  },
};

document.addEventListener("DOMContentLoaded", async (e) => {
  const result = await navigator.runAdAuction(auctionConfig);
  console.log(result);

  if (result) {
    let fencedFrameWithAd = document.createElement("fencedframe");
    fencedFrameWithAd.src = result;
    fencedFrameWithAd.setAttribute("width", "400");
    fencedFrameWithAd.setAttribute("height", "100");
    fencedFrameWithAd.setAttribute("mode", "opaque-ads");
    document.body.appendChild(fencedFrameWithAd);
  } else {
    document.body.innerText = "Nothing to show";
  }
});

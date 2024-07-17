import { Wallet, CrossClient, types, Exchange } from "@zetamarkets/sdk";
import { Keypair, Connection, PublicKey } from "@solana/web3.js";
import { assetToIndex } from "@zetamarkets/sdk/dist/assets";
import { toNetwork } from "@zetamarkets/sdk/dist/network";
import minimist from "minimist";
import { exchange } from "@zetamarkets/sdk/dist/exchange";

async function main() {
  const argv = minimist(process.argv.slice(2));

  const endpoint: string = argv.endpoint;
  const network: string = argv.network || "mainnet";
  const userWalletKey: string = argv.user_pubkey;
  console.log(
    `Endpoint: ${endpoint}, Network: ${network}, UserWalletKey: ${userWalletKey}`,
  );

  const user_key = Keypair.generate();
  const wallet = new Wallet(user_key);
  const userWalletPublicKey = new PublicKey(userWalletKey);

  const connection: Connection = new Connection(endpoint, "confirmed");
  const loadExchangeConfig = types.defaultLoadExchangeConfig(
    toNetwork(network),
    connection,
  );

  await Exchange.load(loadExchangeConfig);
  const client = await CrossClient.load(
    connection,
    wallet,
    undefined,
    undefined,
    undefined,
    userWalletPublicKey,
  );

  exchange.assets.forEach((asset) => {
    const riskData = Exchange.riskCalculator.getEstimatedLiquidationPrice(
      asset,
      client.account!,
    );
    console.log(
      `Asset: ${asset}, Index: ${assetToIndex(asset)}, Liquidation_Price: ${riskData}`,
    );
  });

  process.exit(0);
}

main().catch(console.error.bind(console));

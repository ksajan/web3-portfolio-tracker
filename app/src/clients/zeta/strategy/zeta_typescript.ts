
import { Wallet, CrossClient, types, Exchange, Network, risk } from '@zetamarkets/sdk'
import { Keypair, Connection, PublicKey } from '@solana/web3.js'
import { Asset } from '@zetamarkets/sdk/dist/constants';


async function main() {

    const user_key = Keypair.generate();
    const wallet = new Wallet(user_key);

    const connection: Connection = new Connection('https://mainnet.helius-rpc.com/?api-key=27428150-2aee-44d7-a016-6a465d22f926', 'confirmed');
    const loadExchangeConfig = types.defaultLoadExchangeConfig(
        Network.MAINNET,
        connection
    );


    await Exchange.load(loadExchangeConfig);
    const client = await CrossClient.load(connection, wallet, undefined, undefined, undefined, new PublicKey('BvDMnDXHxw8dLTyfMJWwsZVWsAGzYfJrUak1W3uJ76R4'));

    const riskData = Exchange.riskCalculator.getEstimatedLiquidationPrice(Asset.ONEMBONK, client.account!);
    console.log("liquidation_price=", riskData);
    await Exchange.close();
    await client.close();


}

main().catch(console.error.bind(console));

import time
from web3 import Web3

# Konfigurasi URL RPC
RPC_URL = 'https://hybrid-testnet.rpc.caldera.xyz/http'

# Private key Anda
PRIVATE_KEY = '26bb674281e0a202edea424c7da4ecedbe25d8bf7ceb5ece6c016f7eb021b6bb'

# Alamat penerima
RECIPIENT_ADDRESS = '0x0000000000000000000000000000000000000064'

# Signature dari metode yang ingin dipanggil
METHOD_SIGNATURE = '0x25e16063000000000000000000000000a7c9cf0236cc04b48194013924abc1478fd6d439'

# Inisialisasi Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Mengecek koneksi
if not web3.is_connected():
    print("Gagal terhubung ke jaringan Ethereum.")
    exit()

# Mendapatkan alamat dari private key
account = web3.eth.account.from_key(PRIVATE_KEY)
address = account.address
print(f'Connected to address: {address}')

while True:
    try:
        # Mengambil saldo
        balance = web3.eth.get_balance(address)
        print(f'Saldo: {web3.from_wei(balance, "ether")} ETH')

        # Mengirim transaksi
        nonce = web3.eth.get_transaction_count(address)
        gas_price = web3.eth.gas_price

        # Mendapatkan estimasi gas untuk transaksi
        gas_estimate = web3.eth.estimate_gas({
            'to': RECIPIENT_ADDRESS,
            'data': METHOD_SIGNATURE
        })

        # Membuat transaksi
        transaction = {
            'to': RECIPIENT_ADDRESS,
            'value': web3.to_wei(0, 'ether'),  # Tidak mengirim Ether, hanya data
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': 1225,  # ID chain yang sesuai
            'data': METHOD_SIGNATURE  # Data untuk transaksi
        }

        # Menandatangani transaksi
        signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

        # Mengirim transaksi
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        txn_hash_hex = web3.to_hex(txn_hash)
        print(f'Transaksi dikirim dengan hash: {txn_hash_hex}')

        # Memeriksa status transaksi
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        # Menampilkan informasi transaksi
        print(f'Transaksi berhasil dengan status: {txn_receipt.status}')
        print(f'Gas digunakan: {txn_receipt.gasUsed}')

        # Tunggu sebelum mengulangi transaksi
        time.sleep(5)  # Ubah sesuai kebutuhan, misalnya 12 detik

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        # Mengabaikan kesalahan dan melanjutkan ke iterasi berikutnya
        continue
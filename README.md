# HYPERVN SpigotMC Update Notifier

Tu kiem tra phien ban resource **TuTienCore** tren SpigotMC (resource ID: `139171`) moi 10 phut va gui Discord Embed khi phat hien phien ban moi.

## Thiet lap Discord webhook
1. Mo repository **Settings > Secrets and variables > Actions**.
2. Chon **New repository secret**.
3. Dat ten chinh xac la `DISCORD_WEBHOOK`.
4. Dan URL webhook Discord moi vao o Secret roi luu.

> Khong commit webhook URL vao source code, README hoac file cong khai.

## Chay lan dau
1. Mo tab **Actions**.
2. Chon workflow **SpigotMC Update Notifier**.
3. Nhan **Run workflow**.

Lan chay dau tien chi luu phien ban hien tai lam moc, khong gui thong bao. Nhung lan sau chi gui khi phien ban thay doi.

## Thanh phan
- `.github/workflows/spigot-update.yml`: lich chay GitHub Actions.
- `notifier.py`: kiem tra phien ban va gui Discord Embed.
- `last_version.txt`: duoc tao/cap nhat tu dong sau lan chay.

Resource: https://www.spigotmc.org/resources/139171/

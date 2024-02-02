/*Table structure for table `tbl_buku` */
DROP TABLE IF EXISTS `tbl_buku`;
CREATE TABLE `tbl_buku` (
  `id_buku` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `judul_buku` varchar(100) NOT NULL,
  `tahun_terbit` int(4) NOT NULL,
  `penerbit` varchar(30) NOT NULL,
  `penulis` varchar(30) NOT NULL,
  `id_kategori` int(3) NOT NULL,
  `isdeleted` tinyint(1) NOT NULL DEFAULT 0
);

/*Data for the table `tbl_buku` */
INSERT INTO `tbl_buku` VALUES 
(1,'Pintar Matematika',2015,'Erlangga','Jarno',1,0),
(2,'Hidup Sehat Sejati',2020,'Erlangga','Jino',1,1),
(3,'Kisah 1002',2020,'Bentang Pustaka','Andrea Hirata',2,1),
(4,'Kisah 1002',2020,'Bentang Pustaka','Andrea Hirata',2,1),
(5,'Kisah 1004',2020,'Bentang Pustaka','Andrea Hirata',2,1),
(6,'Ayah',2015,'Bentang Pustaka','Andrea Hirata',2,1),
(7,'Habis Gelap Terbitlah Terang',1997,'Gramedia','Anom',1,0),
(8,'Peraih Mimpi',2000,'Bentang Pustaka','Tere Liye',2,1),
(9,'Ayat Cinta',2000,'Gramedia','Arman',2,0),
(10,'Buku Matematika',2020,'Erlangga','Arya',1,0),
(12,'Hidup Sehat',2020,'Bentang Pustaka','Anom',1,1);

/*Table structure for table `tbl_kategori` */
DROP TABLE IF EXISTS `tbl_kategori`;
CREATE TABLE `tbl_kategori` (
  `id_kategori` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `nama_kategori` varchar(30) NOT NULL,
  `isdeleted` tinyint(1) NOT NULL DEFAULT 0
);

/*Data for the table `tbl_kategori` */
INSERT INTO `tbl_kategori` VALUES 
(1,'Buku Pelajaran',0),
(2,'Novel',0),
(3,'Komik',0);

/*Table structure for table `tbl_member` */
DROP TABLE IF EXISTS `tbl_member`;
CREATE TABLE `tbl_member` (
  `id_member` varchar(30) NOT NULL PRIMARY KEY,
  `nama_member` varchar(100) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `email` varchar(50) NOT NULL,
  `no_telp` varchar(15) NOT NULL,
  `created` TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

/*Data for the table `tbl_member` */
INSERT INTO `tbl_member` VALUES 
('M-2010001','Dharma','Jrakah 02/04','dharma.bekti16696@gmail.com','2129019201', '2020-11-15 19:57:39'  ),
('M-2010002','Anom','Janti','dharma.bekti166@gmail.com','21291029', '2020-11-15 19:57:39');

/*Table structure for table `tbl_peminjaman` */
DROP TABLE IF EXISTS `tbl_peminjaman`;
CREATE TABLE `tbl_peminjaman` (
  `id_peminjaman` varchar(30) NOT NULL PRIMARY KEY,
  `id_member` varchar(30) NOT NULL,
  `id_user` INTEGER NOT NULL,
  `id_buku` INTEGER NOT NULL,
  `tgl_pinjam` TEXT NOT NULL,
  `tgl_kembali` TEXT DEFAULT NULL,
  `status_pinjam` varchar(15) NOT NULL
);

/*Data for the table `tbl_peminjaman` */

/*Table structure for table `tbl_role` */
DROP TABLE IF EXISTS `tbl_role`;
CREATE TABLE `tbl_role` (
  `id_role` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `nama_role` varchar(30) NOT NULL
);

/*Data for the table `tbl_role` */
INSERT INTO `tbl_role` VALUES 
(1,'Manajer'),
(2,'Pustakawan');

/*Table structure for table `tbl_user` */
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user` (
  `id_user` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `nama_user` varchar(50) NOT NULL,
  `username` varchar(30) NOT NULL,
  `id_role` INTEGER NOT NULL,
  `password` varchar(255) NOT NULL,
  `isdeleted` tinyint(1) NOT NULL DEFAULT 0
);

/*Data for the table `tbl_user` */
INSERT INTO `tbl_user` VALUES 
(1,'Manager','manager',1,'b456f30873e3fbbe70dbb2e6775843d90eb5a8fb471b1b42698de889783a4d10b95f1f8114e31f970d9b71439e5ff0d281a131f0a4d061e7a81b4c69f279325f',0),
(2,'Pustakawan','pustakawan',2,'b456f30873e3fbbe70dbb2e6775843d90eb5a8fb471b1b42698de889783a4d10b95f1f8114e31f970d9b71439e5ff0d281a131f0a4d061e7a81b4c69f279325f',0),
(3,'Bekti','bekti',1,'b456f30873e3fbbe70dbb2e6775843d90eb5a8fb471b1b42698de889783a4d10b95f1f8114e31f970d9b71439e5ff0d281a131f0a4d061e7a81b4c69f279325f',0);

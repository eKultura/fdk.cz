-- Adminer 4.7.8 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

USE `fdk_db`;

SET NAMES utf8mb4;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1,	'Can add log entry',	1,	'add_logentry'),
(2,	'Can change log entry',	1,	'change_logentry'),
(3,	'Can delete log entry',	1,	'delete_logentry'),
(4,	'Can view log entry',	1,	'view_logentry'),
(5,	'Can add permission',	2,	'add_permission'),
(6,	'Can change permission',	2,	'change_permission'),
(7,	'Can delete permission',	2,	'delete_permission'),
(8,	'Can view permission',	2,	'view_permission'),
(9,	'Can add group',	3,	'add_group'),
(10,	'Can change group',	3,	'change_group'),
(11,	'Can delete group',	3,	'delete_group'),
(12,	'Can view group',	3,	'view_group'),
(13,	'Can add user',	4,	'add_user'),
(14,	'Can change user',	4,	'change_user'),
(15,	'Can delete user',	4,	'delete_user'),
(16,	'Can view user',	4,	'view_user'),
(17,	'Can add content type',	5,	'add_contenttype'),
(18,	'Can change content type',	5,	'change_contenttype'),
(19,	'Can delete content type',	5,	'delete_contenttype'),
(20,	'Can view content type',	5,	'view_contenttype'),
(21,	'Can add session',	6,	'add_session'),
(22,	'Can change session',	6,	'change_session'),
(23,	'Can delete session',	6,	'delete_session'),
(24,	'Can view session',	6,	'view_session'),
(25,	'Can add user',	7,	'add_user'),
(26,	'Can change user',	7,	'change_user'),
(27,	'Can delete user',	7,	'delete_user'),
(28,	'Can view user',	7,	'view_user'),
(29,	'Can add comment',	8,	'add_comment'),
(30,	'Can change comment',	8,	'change_comment'),
(31,	'Can delete comment',	8,	'delete_comment'),
(32,	'Can view comment',	8,	'view_comment'),
(33,	'Can add activity_log',	9,	'add_activity_log'),
(34,	'Can change activity_log',	9,	'change_activity_log'),
(35,	'Can delete activity_log',	9,	'delete_activity_log'),
(36,	'Can view activity_log',	9,	'view_activity_log'),
(37,	'Can add list',	10,	'add_list'),
(38,	'Can change list',	10,	'change_list'),
(39,	'Can delete list',	10,	'delete_list'),
(40,	'Can view list',	10,	'view_list'),
(41,	'Can add milestone',	11,	'add_milestone'),
(42,	'Can change milestone',	11,	'change_milestone'),
(43,	'Can delete milestone',	11,	'delete_milestone'),
(44,	'Can view milestone',	11,	'view_milestone'),
(45,	'Can add task',	12,	'add_task'),
(46,	'Can change task',	12,	'change_task'),
(47,	'Can delete task',	12,	'delete_task'),
(48,	'Can view task',	12,	'view_task'),
(49,	'Can add category',	13,	'add_category'),
(50,	'Can change category',	13,	'change_category'),
(51,	'Can delete category',	13,	'delete_category'),
(52,	'Can view category',	13,	'view_category'),
(53,	'Can add document',	14,	'add_document'),
(54,	'Can change document',	14,	'change_document'),
(55,	'Can delete document',	14,	'delete_document'),
(56,	'Can view document',	14,	'view_document'),
(57,	'Can add project',	15,	'add_project'),
(58,	'Can change project',	15,	'change_project'),
(59,	'Can delete project',	15,	'delete_project'),
(60,	'Can view project',	15,	'view_project'),
(61,	'Can add list_item',	16,	'add_list_item'),
(62,	'Can change list_item',	16,	'change_list_item'),
(63,	'Can delete list_item',	16,	'delete_list_item'),
(64,	'Can view list_item',	16,	'view_list_item'),
(65,	'Can add attachment',	17,	'add_attachment'),
(66,	'Can change attachment',	17,	'change_attachment'),
(67,	'Can delete attachment',	17,	'delete_attachment'),
(68,	'Can view attachment',	17,	'view_attachment'),
(69,	'Can add flist',	10,	'add_flist'),
(70,	'Can change flist',	10,	'change_flist'),
(71,	'Can delete flist',	10,	'delete_flist'),
(72,	'Can view flist',	10,	'view_flist'),
(73,	'Can add contact',	18,	'add_contact'),
(74,	'Can change contact',	18,	'change_contact'),
(75,	'Can delete contact',	18,	'delete_contact'),
(76,	'Can view contact',	18,	'view_contact'),
(77,	'Can add contract',	19,	'add_contract'),
(78,	'Can change contract',	19,	'change_contract'),
(79,	'Can delete contract',	19,	'delete_contract'),
(80,	'Can view contract',	19,	'view_contract'),
(81,	'Can add item',	20,	'add_item'),
(82,	'Can change item',	20,	'change_item'),
(83,	'Can delete item',	20,	'delete_item'),
(84,	'Can view item',	20,	'view_item'),
(85,	'Can add transaction',	21,	'add_transaction'),
(86,	'Can change transaction',	21,	'change_transaction'),
(87,	'Can delete transaction',	21,	'delete_transaction'),
(88,	'Can view transaction',	21,	'view_transaction'),
(89,	'Can add warehouse',	22,	'add_warehouse'),
(90,	'Can change warehouse',	22,	'change_warehouse'),
(91,	'Can delete warehouse',	22,	'delete_warehouse'),
(92,	'Can view warehouse',	22,	'view_warehouse'),
(93,	'Can add project_user',	23,	'add_project_user'),
(94,	'Can change project_user',	23,	'change_project_user'),
(95,	'Can delete project_user',	23,	'delete_project_user'),
(96,	'Can view project_user',	23,	'view_project_user'),
(97,	'Can add role',	24,	'add_role'),
(98,	'Can change role',	24,	'change_role'),
(99,	'Can delete role',	24,	'delete_role'),
(100,	'Can view role',	24,	'view_role'),
(101,	'Can add role_permission',	25,	'add_role_permission'),
(102,	'Can change role_permission',	25,	'change_role_permission'),
(103,	'Can delete role_permission',	25,	'delete_role_permission'),
(104,	'Can view role_permission',	25,	'view_role_permission'),
(105,	'Can add permission',	26,	'add_permission'),
(106,	'Can change permission',	26,	'change_permission'),
(107,	'Can delete permission',	26,	'delete_permission'),
(108,	'Can view permission',	26,	'view_permission'),
(109,	'Can add list_permission',	27,	'add_list_permission'),
(110,	'Can change list_permission',	27,	'change_list_permission'),
(111,	'Can delete list_permission',	27,	'delete_list_permission'),
(112,	'Can view list_permission',	27,	'view_list_permission'),
(113,	'Can add test_error',	28,	'add_test_error'),
(114,	'Can change test_error',	28,	'change_test_error'),
(115,	'Can delete test_error',	28,	'delete_test_error'),
(116,	'Can view test_error',	28,	'view_test_error'),
(117,	'Can add test_type',	29,	'add_test_type'),
(118,	'Can change test_type',	29,	'change_test_type'),
(119,	'Can delete test_type',	29,	'delete_test_type'),
(120,	'Can view test_type',	29,	'view_test_type'),
(121,	'Can add test_result',	30,	'add_test_result'),
(122,	'Can change test_result',	30,	'change_test_result'),
(123,	'Can delete test_result',	30,	'delete_test_result'),
(124,	'Can view test_result',	30,	'view_test_result'),
(125,	'Can add test',	31,	'add_test'),
(126,	'Can change test',	31,	'change_test'),
(127,	'Can delete test',	31,	'delete_test'),
(128,	'Can view test',	31,	'view_test'),
(129,	'Can add company',	32,	'add_company'),
(130,	'Can change company',	32,	'change_company'),
(131,	'Can delete company',	32,	'delete_company'),
(132,	'Can view company',	32,	'view_company'),
(133,	'Can add invoice',	33,	'add_invoice'),
(134,	'Can change invoice',	33,	'change_invoice'),
(135,	'Can delete invoice',	33,	'delete_invoice'),
(136,	'Can view invoice',	33,	'view_invoice'),
(137,	'Can add invoice_item',	34,	'add_invoice_item'),
(138,	'Can change invoice_item',	34,	'change_invoice_item'),
(139,	'Can delete invoice_item',	34,	'delete_invoice_item'),
(140,	'Can view invoice_item',	34,	'view_invoice_item'),
(141,	'Can add attachment',	35,	'add_attachment'),
(142,	'Can change attachment',	35,	'change_attachment'),
(143,	'Can delete attachment',	35,	'delete_attachment'),
(144,	'Can view attachment',	35,	'view_attachment');

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1,	'pbkdf2_sha256$870000$fourBRqFf9lS4YHkCkl9AD$uJe11tRFqa9WpDYVqHPqDkT4nepANT5n05kIT81xyFs=',	'2025-02-22 12:15:41.854197',	1,	'martin',	'Martin',	'Kučera',	'',	1,	1,	'2024-09-06 19:38:07.869976'),
(2,	'pbkdf2_sha256$870000$jvf8GuMa6SkvukEDWi6O9z$BG4GHmSyjA88pTl1aWI7aKEpa8a1igvN1CE8PY8hVNQ=',	'2024-10-30 09:58:05.126600',	0,	'martin2',	'',	'',	'martin2@div.cz',	0,	1,	'2024-09-09 20:35:14.389849'),
(5,	'pbkdf2_sha256$870000$lfvjb2mTxUo11nZXxyNnpl$NoFrGds0zcB/HAhdwk2u/lmMAZKVg7Wgy9JNM88Zu3A=',	'2024-09-11 17:33:19.476983',	0,	'martin5',	'',	'',	'marti@aa.cz',	0,	1,	'2024-09-11 17:33:19.120506'),
(6,	'pbkdf2_sha256$870000$yxWv0N7MYoH91J6swk6uiE$Dd3gnzIOx2W18PNHedaFyUv47gso2JTQULzL9Hrqm+I=',	'2024-10-26 05:51:38.480320',	0,	'martin9',	'',	'',	'martin@div.cz',	0,	1,	'2024-09-13 17:36:20.310555'),
(7,	'pbkdf2_sha256$870000$Y14ZU0uZfmxTIGv9K8MyeR$MN1cj1y2in7ehkvs/t77NcDQXnZ6xRtrDZdA6/CNbJE=',	'2024-11-20 09:03:13.460028',	0,	'Lenka',	'',	'',	'Lenka_Frankova@outlook.com',	0,	1,	'2024-09-24 19:03:12.949532'),
(8,	'pbkdf2_sha256$870000$FPCCmhjqrpvBBUxYWLBiHm$BEJs8swnyueNydUxAYKyGY1w/IHMYWzuIHmXAAQDIL8=',	'2024-10-02 14:59:19.686005',	0,	'martin.kucera',	'',	'',	'veronika@kucerova2.eu',	0,	1,	'2024-10-02 14:59:19.358277'),
(9,	'pbkdf2_sha256$870000$sKt6msk7wAf2n7C1M2176P$3zGBlqIXd34Y9+1XDrQIXUHpkN7vgMthHy7piSq2+lI=',	'2024-10-26 07:13:44.647619',	0,	'Fafol',	'Martin',	'',	'',	0,	1,	'2024-10-26 07:13:44.324611'),
(10,	'pbkdf2_sha256$870000$qNRA3zATqMe4L63NkkYjjD$b0j4Bq+W+iXJ/w/x85PIEO2WtYKL3Y4kX1pUOYseTGs=',	'2024-10-28 14:15:55.097811',	0,	'testik',	'Martin',	'Kučera',	'media@ekultura.eu',	0,	1,	'2024-10-26 07:54:44.496202'),
(11,	'pbkdf2_sha256$870000$VCzHhcWETO9nU0x23ojDKH$r8/x2VadyMOn0vEm3L2lhA6wTM/fY5uBprp5wXJ4DYQ=',	'2024-10-27 20:07:16.844839',	0,	'Baruuuuuu',	'',	'',	'ohnivacek123@gmail.com',	0,	1,	'2024-10-27 20:07:16.500581'),
(12,	'pbkdf2_sha256$870000$PHobJN4xe7cd7ix9g7tgFZ$4cKsHSxRExn0N664WfHOxhP03lAuo4G32GGuQ8PU3ZE=',	'2025-02-01 20:17:32.168032',	0,	'werru',	'',	'',	'lamune02@gmail.com',	0,	1,	'2024-10-29 18:13:31.148403'),
(13,	'pbkdf2_sha256$870000$PgGYPdGF65Q4FhnaY6zV3r$A2ICvwuE6Kr+IG90SaRl+GzaSW6n7PKR1+dkpwD4kIQ=',	'2024-11-30 09:47:27.171580',	0,	'ionno',	'',	'',	'illnezz@centrum.cz',	0,	1,	'2024-10-29 20:57:12.007400'),
(14,	'pbkdf2_sha256$870000$iYm2yzfH8wzeZgdOBMpQFj$9p8JF4hahlpKYDVQfgdXTgRIxsvdZqyc6KGjZPdjBew=',	'2024-10-29 21:05:20.089147',	0,	'martin10',	'',	'',	'martin@esmobil.cz',	0,	1,	'2024-10-29 21:05:19.759023'),
(15,	'pbkdf2_sha256$870000$taokRGdeU7aTa3wLN3kBju$h/U1R/iN6LVRzt6hdwFdHDcouRq8Np08LQJS7vvKpF0=',	'2024-10-30 17:54:32.186704',	0,	'Misa',	'',	'',	'aellea.lipenska@gmail.com',	0,	1,	'2024-10-30 17:54:31.853748'),
(16,	'pbkdf2_sha256$870000$p1yaqGqbkw8B6WsCUWKZ3e$Y8pxFnVxgkInzPKj9NRBipc2GhlZXqQPqC3NwPH8fXw=',	'2025-01-23 09:14:35.411717',	0,	'Bershee',	'',	'',	'berankovap90@gmail.com',	0,	1,	'2024-10-30 18:12:10.379660'),
(17,	'pbkdf2_sha256$870000$kPVfIlk8tL1gzmfwc8iYN4$ldK9rKTyKS/u4PUhA+e2pSy0U2K8fCW51Uu3y5Vw3gw=',	'2024-10-30 18:38:57.817567',	0,	'PetrHrdina',	'',	'',	'shorty.one@seznam.cz',	0,	1,	'2024-10-30 18:32:40.553791'),
(18,	'pbkdf2_sha256$870000$RiHnFxdwQrD0DSzhYV9pQZ$RHN5a+Hc7lsm3slUOpynWlImp1wTHixpi5GaW/WOZQ0=',	'2024-11-16 12:05:30.327564',	0,	'SimonR',	'',	'',	'masmer01@yahoo.com',	0,	1,	'2024-11-16 12:05:29.975786'),
(19,	'pbkdf2_sha256$870000$k9GbSwB1YwwPZxfCqqcfHb$kBp8QfMqb3bSmln2cf2ZB6HNoq1CYoYCI05Th27AQKY=',	'2024-11-17 18:00:50.093057',	0,	'juraj',	'',	'',	'a@a.com',	0,	1,	'2024-11-17 18:00:49.709915'),
(20,	'pbkdf2_sha256$870000$vpWkTLZxiplNfM8q4I3zM2$Au9YIOTLUBwPMiZ7kABZiAX0ULG3tG+LVjyODQ+22w4=',	'2025-02-22 12:26:37.181618',	0,	'VendaCiki',	'',	'',	'vendaciki@seznam.cz',	0,	1,	'2024-11-18 18:02:10.472443'),
(21,	'pbkdf2_sha256$870000$RKipLUwBPFURWMuugCNb3u$c3e2siIQaKzi0GNenR1FyNiUqzOLQWIrGLK5KFuJHNs=',	'2024-12-08 10:49:13.112881',	0,	'xsilence8x',	'',	'',	'xsilence8x@hotmail.com',	0,	1,	'2024-11-22 08:25:21.954966'),
(24,	'pbkdf2_sha256$870000$DzpwmO3anzCPB9MjPJil8b$HHFvEh6SvnPhkt28LrNAL6WeJeOnhbBQj7ajwi2H1Ps=',	'2024-11-24 11:50:37.780037',	0,	'jirka',	'',	'',	'jirkha13@gmail.com',	0,	1,	'2024-11-24 11:50:37.415046'),
(25,	'pbkdf2_sha256$870000$nyRmHHBuHTUiXBXYMvCSUO$gcGUkp7zyAvadGQEiYSoEAMi+Nuf3F2jSJdkpwq2EUk=',	'2024-11-26 05:51:02.821206',	0,	'Testtest',	'',	'',	'martin@martin.ma',	0,	1,	'2024-11-26 05:51:02.437239'),
(26,	'pbkdf2_sha256$870000$g9Cs44kjaNN5Ktcwuoh9ho$er9fmEeFeNXjVY0ax4E95zXzAhe/2dt72WvPCPvvazg=',	'2024-12-02 12:49:50.579959',	0,	'JanaS',	'',	'',	'Jana.sot@seznam.cz',	0,	1,	'2024-11-26 06:38:36.933707'),
(27,	'pbkdf2_sha256$870000$tjg2tNbvu86hejCOPK4lOa$uSNYRFQjTVarpDNwBDAUoN4TIVZkDfI1bKZeuTFvFbE=',	'2025-01-20 19:42:39.608724',	0,	'lascalca',	'',	'',	'kkasalova.professional@gmail.com',	0,	1,	'2024-11-26 08:38:37.149890'),
(28,	'pbkdf2_sha256$870000$r8VXoXAHu5JttQPwAGG2ad$OG2hOmvOnanYa3FQ3Vk0yYws1ENgI/NII3QC0aj0Rho=',	'2024-11-27 16:59:56.227977',	0,	'SonaJirotova',	'',	'',	'sjirotova@seznam.cz',	0,	1,	'2024-11-27 16:59:55.878562'),
(29,	'pbkdf2_sha256$870000$5YsHcWAO1Ea3GID5447ijp$jxiOgJ0E4Qwov6nvWTWjk5iS4rQ9HhCLgD81FhSNZy8=',	'2024-12-18 14:35:25.533437',	0,	'Martin22',	'',	'',	'martin1.kucera@t-mobile.cz',	0,	1,	'2024-12-18 14:35:24.824049'),
(30,	'pbkdf2_sha256$870000$Lzhht6gBcW6IVDRiipTspq$hPoewrGTfEsgqOy/tSCstO3uEps5NenpIELOScdXiLI=',	'2025-01-11 16:46:51.520760',	0,	'Donaldalimi',	'',	'',	'donetsk-minsk@bin-bamg.store',	0,	1,	'2025-01-11 16:46:51.153409'),
(31,	'pbkdf2_sha256$870000$gi7vxerwNZTsruzDHxKqa1$yZ4N0BdURPn2mKdoRmp51JJ4eCYLrTfKMbCxW41AmPY=',	'2025-01-11 16:47:52.493951',	0,	'Shawnsum',	'',	'',	'poezdki-v-rostov@bin-bamg.store',	0,	1,	'2025-01-11 16:47:52.108665'),
(32,	'pbkdf2_sha256$870000$vMoad08TRVMJwk9d9jYCmu$SEJyorQIo8MBjWVSuyL7vX1bepN40occbBXTFsc0ubM=',	'2025-01-11 20:09:04.592949',	0,	'WoodrowFaimb',	'',	'',	'festore@bin-bamg.store',	0,	1,	'2025-01-11 20:09:04.231449'),
(33,	'pbkdf2_sha256$870000$Gow9rQm17PDfOtRk0I5LZL$eV7r1xifgOGZWKElSj678QUYgoPEj8QTS1wCwrpfd3E=',	'2025-01-22 00:47:28.449013',	0,	'Dennistuh',	'',	'',	'uslugi_advokata@bin-bamg.ru',	0,	1,	'2025-01-22 00:47:28.056294'),
(34,	'pbkdf2_sha256$870000$ufVtDJdM4mcqiDVIAVimQ9$TB7YOoKOkvXmr3nNYi/SG3TkKHGiTEaAclKTZIAm3y4=',	'2025-02-06 16:46:55.256736',	0,	'RonaldNiz',	'',	'',	'festore@bin-bamg.ru',	0,	1,	'2025-02-06 16:46:54.851093'),
(35,	'pbkdf2_sha256$870000$T4H4C1Zdpu3jJowuLUU3Dc$vK98HaHwIT4OaQaofAmUcbOnSiESYVp855nr0IgZmNs=',	'2025-02-06 16:47:30.204597',	0,	'Walternix',	'',	'',	'donetsk-minsk@bin-bamg.ru',	0,	1,	'2025-02-06 16:47:29.847474');

DELIMITER ;;

CREATE TRIGGER `after_user_insert` AFTER INSERT ON `auth_user` FOR EACH ROW
BEGIN
    -- Vloží nový záznam do FDK_users při registraci nového uživatele
    INSERT INTO FDK_users (username, password_hash, email, created, last_login)
    VALUES (
        NEW.username,           -- Uloží username z auth_user
        NEW.password,           -- Uloží zahashované heslo z auth_user
        NEW.email,              -- Uloží email z auth_user
        NEW.date_joined,        -- Uloží datum registrace z auth_user
        NEW.last_login          -- Uloží datum posledního přihlášení z auth_user (může být NULL)
    );
END;;

DELIMITER ;

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1,	'admin',	'logentry'),
(3,	'auth',	'group'),
(2,	'auth',	'permission'),
(4,	'auth',	'user'),
(5,	'contenttypes',	'contenttype'),
(35,	'django_summernote',	'attachment'),
(9,	'fdk_cz',	'activity_log'),
(17,	'fdk_cz',	'attachment'),
(13,	'fdk_cz',	'category'),
(8,	'fdk_cz',	'comment'),
(32,	'fdk_cz',	'company'),
(18,	'fdk_cz',	'contact'),
(19,	'fdk_cz',	'contract'),
(14,	'fdk_cz',	'document'),
(10,	'fdk_cz',	'flist'),
(33,	'fdk_cz',	'invoice'),
(34,	'fdk_cz',	'invoice_item'),
(20,	'fdk_cz',	'item'),
(16,	'fdk_cz',	'list_item'),
(27,	'fdk_cz',	'list_permission'),
(11,	'fdk_cz',	'milestone'),
(26,	'fdk_cz',	'permission'),
(15,	'fdk_cz',	'project'),
(23,	'fdk_cz',	'project_user'),
(24,	'fdk_cz',	'role'),
(25,	'fdk_cz',	'role_permission'),
(12,	'fdk_cz',	'task'),
(31,	'fdk_cz',	'test'),
(28,	'fdk_cz',	'test_error'),
(30,	'fdk_cz',	'test_result'),
(29,	'fdk_cz',	'test_type'),
(21,	'fdk_cz',	'transaction'),
(7,	'fdk_cz',	'user'),
(22,	'fdk_cz',	'warehouse'),
(6,	'sessions',	'session');

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1,	'contenttypes',	'0001_initial',	'2024-09-06 19:37:26.319120'),
(2,	'auth',	'0001_initial',	'2024-09-06 19:37:26.655545'),
(3,	'admin',	'0001_initial',	'2024-09-06 19:37:26.727499'),
(4,	'admin',	'0002_logentry_remove_auto_add',	'2024-09-06 19:37:26.734822'),
(5,	'admin',	'0003_logentry_add_action_flag_choices',	'2024-09-06 19:37:26.741274'),
(6,	'contenttypes',	'0002_remove_content_type_name',	'2024-09-06 19:37:26.798627'),
(7,	'auth',	'0002_alter_permission_name_max_length',	'2024-09-06 19:37:26.832816'),
(8,	'auth',	'0003_alter_user_email_max_length',	'2024-09-06 19:37:26.854861'),
(9,	'auth',	'0004_alter_user_username_opts',	'2024-09-06 19:37:26.861562'),
(10,	'auth',	'0005_alter_user_last_login_null',	'2024-09-06 19:37:26.894285'),
(11,	'auth',	'0006_require_contenttypes_0002',	'2024-09-06 19:37:26.895818'),
(12,	'auth',	'0007_alter_validators_add_error_messages',	'2024-09-06 19:37:26.903626'),
(13,	'auth',	'0008_alter_user_username_max_length',	'2024-09-06 19:37:26.925048'),
(14,	'auth',	'0009_alter_user_last_name_max_length',	'2024-09-06 19:37:26.945257'),
(15,	'auth',	'0010_alter_group_name_max_length',	'2024-09-06 19:37:26.965243'),
(16,	'auth',	'0011_update_proxy_permissions',	'2024-09-06 19:37:26.971592'),
(17,	'auth',	'0012_alter_user_first_name_max_length',	'2024-09-06 19:37:26.993654'),
(18,	'sessions',	'0001_initial',	'2024-09-06 19:37:27.025980'),
(19,	'fdk_cz',	'0001_initial',	'2024-09-07 16:01:45.525343'),
(20,	'fdk_cz',	'0002_alter_project_owner',	'2024-09-11 20:05:03.410088'),
(21,	'fdk_cz',	'0003_rename_list_flist_rename_list_list_item_flist',	'2024-09-12 12:57:07.578425'),
(22,	'fdk_cz',	'0004_alter_activity_log_user_alter_comment_user_and_more',	'2024-09-12 13:39:24.514178'),
(23,	'fdk_cz',	'0005_alter_list_item_created',	'2024-09-12 13:41:01.712731'),
(24,	'fdk_cz',	'0006_alter_list_item_created',	'2024-09-12 13:44:00.161339'),
(25,	'fdk_cz',	'0007_alter_flist_modified',	'2024-09-12 13:45:00.735478'),
(26,	'fdk_cz',	'0008_item_warehouse_contact_contract_transaction_and_more',	'2024-09-13 09:27:11.066510'),
(27,	'fdk_cz',	'0009_alter_contract_table_alter_item_table_and_more',	'2024-09-13 09:29:20.548769'),
(28,	'fdk_cz',	'0010_alter_item_table_alter_transaction_table_and_more',	'2024-09-13 09:29:55.446195'),
(29,	'fdk_cz',	'0011_permission_role_list_permission_project_user_and_more',	'2024-09-13 18:21:58.761156'),
(30,	'fdk_cz',	'0012_alter_project_user_project_alter_project_user_user',	'2024-09-13 18:36:49.176682'),
(31,	'fdk_cz',	'0013_alter_contact_last_name_alter_list_item_created_and_more',	'2024-09-14 16:21:48.163376'),
(32,	'fdk_cz',	'0014_test_test_result_test_error_test_type_test_test_type',	'2024-09-15 20:47:04.411283'),
(33,	'fdk_cz',	'0015_test_error_date_created_test_error_project_and_more',	'2024-09-15 20:53:44.337731'),
(34,	'fdk_cz',	'0016_alter_flist_created_alter_flist_modified_and_more',	'2024-09-16 15:10:15.070391'),
(35,	'fdk_cz',	'0017_test_error_created_by',	'2024-09-16 17:23:00.543421'),
(36,	'fdk_cz',	'0018_alter_test_error_test_result',	'2024-09-16 18:30:37.726798'),
(37,	'fdk_cz',	'0019_task_parent_alter_test_error_status_and_more',	'2024-09-22 03:52:03.367548'),
(38,	'fdk_cz',	'0020_company_invoice_invoice_item',	'2024-10-05 18:07:02.020465'),
(39,	'fdk_cz',	'0021_invoice_item_vat_rate',	'2024-10-05 18:21:28.726034'),
(40,	'fdk_cz',	'0022_document_category',	'2024-10-27 12:33:02.046540'),
(41,	'fdk_cz',	'0023_task_organization_alter_task_creator',	'2024-11-17 20:24:31.129758'),
(42,	'django_summernote',	'0001_initial',	'2024-11-22 20:30:57.721997'),
(43,	'django_summernote',	'0002_update-help_text',	'2024-11-22 20:30:57.726735'),
(44,	'django_summernote',	'0003_alter_attachment_id',	'2024-11-22 20:30:57.766449'),
(45,	'fdk_cz',	'0024_warehouse_users',	'2024-11-22 22:19:19.098212');

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1j9pt3q7arebooqxi457l92oz74e3yq5',	'.eJxVjEEOwiAQRe_C2pAyCAwu3XsGMsAgVUOT0q6Md7dNutDtf-_9twi0LjWsnecwZnERTpx-t0jpyW0H-UHtPsk0tWUeo9wVedAub1Pm1_Vw_w4q9brVmov10SADWyo6GXQ6qjMiIxkH2iscNNAmOWt9yq4wJPBWDYg6gxOfL9mINxQ:1tDgcD:1WNluCaIMtsDThnnkhYErgZb1c74r3xLT-2HjBZvih8',	'2024-12-04 09:03:13.462889'),
('283f5ql5bqcg9rvrcxcnykcjlarjx3m5',	'.eJxVjEEOwiAQRe_C2pAhU4G6dO8ZyDADUjWQlHbVeHdt0oVu_3vvbyrQupSw9jSHSdRFGVSn3zESP1PdiTyo3pvmVpd5inpX9EG7vjVJr-vh_h0U6uVbA7EwoCBYZ7MhGfIolLIbkjEZPFqOZyHxYNGLEINhB84QIo_JDer9ASi3OK4:1tHK4V:ldu75FpseNq8oh3LnyyWgWPHhtIaBfZz_Kk2hr89BHk',	'2024-12-14 09:47:27.193135'),
('2lo1q3mi847xe3pya2la38pa1xto6z5q',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t6DV2:pnTIscx8fznue95s8Y64gOxoExGoRXsd5tEoHNEpgZk',	'2024-11-13 18:32:56.401145'),
('32utvkc9kukzgbzv5kc6njhdwj0kv64p',	'.eJxVjDsOwjAQBe_iGln-rbOmpM8ZLK8_OIAcKU4qxN1JpBTQvpl5b-bDtla_9bz4KbErU5ZdfkcK8ZnbQdIjtPvM49zWZSJ-KPyknY9zyq_b6f4d1NDrXtsoDAzkrEZbsgEUAEggiKIRgEaiKyiKHqRWijRGTFED7FZ2qJJkny_WQzab:1tI5s6:c0aO3guSbPUTfFqgkcNdBgF46TEJhwvJlC3usoB1fbA',	'2024-12-16 12:49:50.584805'),
('36lc9or27h98upatnbdh572va9g91zvv',	'.eJxVjDsOwjAQBe_iGln-xfZS0ucM1q4_OIAcKU4qxN1JpBTQvpl5bxZwW2vYel7ClNiVacUuvyNhfOZ2kPTAdp95nNu6TMQPhZ-083FO-XU73b-Dir3udYRYisYBjPE2ZRBASUVFQEgWhClQZHE-Gam9sgMIjUr6WHD3nQPJPl8YTDfF:1tWhn6:39ss80cJc1vOsyFvso8B-tsNy0DIhAflorkd03OVy0c',	'2025-01-25 20:09:04.596152'),
('3dq6l37199x39xwy7b3ebdd4ga8c9xan',	'.eJxVjMEOwiAQBf-FsyFAobAevfcbyLJQqRpISnsy_rs06UGvM_Pem3nct-z3lla_RHZl0rDLLwxIz1QOEx9Y7pVTLdu6BH4k_LSNTzWm1-1s_w4yttzXKQ1WAM4aBBlDDiUo6QhstA4CWFKDC0oLg0PqQLtZ4kidSjVqVMA-X_gIN1k:1t6Cts:dE6QLJ_Fj6GHA_411eLhdvgcMwSf_zqrGJYL8sBCVus',	'2024-11-13 17:54:32.189534'),
('3ffnt7nps86gtol6g33sqwg4khadw5sb',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tJ7gS:EGWO2XZGKsIbo28UHXU4c_6L_k-DO1TT7TslhaWCU8U',	'2024-12-19 08:58:04.274151'),
('3l4ugj9qs6ewh4hyrnv9iybshilhg1g0',	'.eJxVjMEOwiAQBf-FsyHAAgWP3v0GArsgVQNJaU_Gf9cmPej1zcx7sRC3tYZt5CXMxM5MKnb6HVPER247oXtst86xt3WZE98VftDBr53y83K4fwc1jvqtQSsdXREYJ5ELApIoptgJsiBnfDFegUugpCEtndEANtsivZKoKEnN3h8AtTdw:1tNzzY:zghJQxz4RGmiyDO68AcHgEHW_vlJ2pG-Y7kgnyGOAF8',	'2025-01-01 19:45:56.630601'),
('3ter9gaguvjg847pdhw7t9e14yqu9t6v',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t5WHM:eNq0IyBTUI5T142bxuC7XHq4bdDWb2BjC5N-SzBjdjU',	'2024-11-11 20:23:56.735314'),
('3tn0122qzlotzlgb3hgpftizxo01t639',	'.eJxVjDsOwjAQRO_iGlm7juMPJX3OYPmzxgFkS3FSIe5OIqWAZop5b-bNnN_W4rZOi5sTuzJEdvktg49PqgdJD1_vjcdW12UO_FD4STufWqLX7XT_DorvZV-bYCyKmKWmUSKNQkMgkFlT8BlMwowCcEiGKEcrI1g9qEHFrITZE9jnCwWDOAs:1t59Xg:J5aQDPO6jHVsyLCXiKNJrtxxSaZHWxnfz4sHcPvQ3LY',	'2024-11-10 20:07:16.847321'),
('3w7mforg19tddi9px64bgi8owlw0sltm',	'.eJxVjEEOwiAQRe_C2pAyCAwu3XsGMsAgVUOT0q6Md7dNutDtf-_9twi0LjWsnecwZnERTpx-t0jpyW0H-UHtPsk0tWUeo9wVedAub1Pm1_Vw_w4q9brVmov10SADWyo6GXQ6qjMiIxkH2iscNNAmOWt9yq4wJPBWDYg6gxOfL9mINxQ:1t4OiP:7rUEphZ0XcSiZrXA0hW9U_f9bdjm8k1j8j69pmLP8Ik',	'2024-11-08 18:07:13.841074'),
('4k3mtb0a2e2bh4hxdfslvmw1nc40bvhx',	'.eJxVjEEOwiAQRe_C2pAyCAwu3XsGMsAgVUOT0q6Md7dNutDtf-_9twi0LjWsnecwZnERTpx-t0jpyW0H-UHtPsk0tWUeo9wVedAub1Pm1_Vw_w4q9brVmov10SADWyo6GXQ6qjMiIxkH2iscNNAmOWt9yq4wJPBWDYg6gxOfL9mINxQ:1stAob:4zaZPR-DFc8KazwgK9MDEijAQB-9YyknLTw1ztuDS9s',	'2024-10-08 19:03:13.305326'),
('4l93j2yvubzlm1zosoixfrv20b0619ss',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t5BTd:JS28AjrvV8chn498AA5pGC36WKduaBYVp8wwdkNhJDI',	'2024-11-10 22:11:13.945072'),
('56n4igvywkjhetlp4zujcdzm9sn71zh4',	'.eJxVjDsOwjAQBe_iGln-fyjpOYPlXXtxADlSnFSIu0OkFNC-mXkvlvK2trSNuqSpsDOTnp1-R8j4qH0n5Z77beY493WZgO8KP-jg17nU5-Vw_w5aHu1bK2nIkSIU1bhsEANKCdqrqJSLBWJA1FoE64uNVkggp4mkroEqKNDs_QEC-zgK:1t6Dar:qDzm0hXZ2s1SojLxllMYPT6Auxv9I8o6PCSdUSpPDvE',	'2024-11-13 18:38:57.820416'),
('58cuor0gyhgc74fodk88lecqji8asrta',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tCHaD:NhAFJeLXFio18wLb6Ae6tGvI8WQbiMizKZUCTBc8BSI',	'2024-11-30 12:07:21.608216'),
('5bta4vt4rj7d1ethte0zbwnpiiq5lgky',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tFpNd:s-x4v06e8MEVZZuBV4aX_tI6GjQVl53r39pO4EIo-bo',	'2024-12-10 06:49:01.662046'),
('5qfmsw9vxf2ym3m4ff7io5ewyutmpq4v',	'.eJxVjDEOwjAMRe-SGUWpQ4rLyM4ZIie2SQGlUtNOiLtDpQ6w_vfef5lI61Li2mSOI5uz6c3hd0uUH1I3wHeqt8nmqS7zmOym2J02e51Ynpfd_Tso1Mq3VgBhyuAYehmUkemYT8KMnkNygRyR7wQ1CzlU9C4Bgg6owXcQgnl_AB9oOL4:1spvYW:dIdtckvCISaPatAJYg-8jHpw0F_V8hz0taoeOSyQGmU',	'2024-09-29 20:09:12.116355'),
('6xy4cf2oj2b5sdc7ah5crtfxabv7zqds',	'.eJxVjEEOwiAQRe_C2pAyCAwu3XsGMsAgVUOT0q6Md7dNutDtf-_9twi0LjWsnecwZnERTpx-t0jpyW0H-UHtPsk0tWUeo9wVedAub1Pm1_Vw_w4q9brVmov10SADWyo6GXQ6qjMiIxkH2iscNNAmOWt9yq4wJPBWDYg6gxOfL9mINxQ:1t2WDu:oI_luQ3RBO2pq09FDymcNHjihosTSrx5WMayG28XMoc',	'2024-11-03 13:43:58.201628'),
('71503azpa7xf02ykx3nf7kxdclq4w6p5',	'.eJxVjEEOwiAQRe_C2hChUMCle89AhhlGqgaS0q6Md7dNutDtf-_9t4iwLiWuPc9xInER-ixOv2MCfOa6E3pAvTeJrS7zlOSuyIN2eWuUX9fD_Tso0MtWIwZLjOy8Sc6RYcOBx5xNsoNTikOipBxmM4AJoEGrwY-OA-Fmk_Xi8wUzwjjq:1tLOXo:R0Z47uhX0elkYWe1HBUZQ4RwdKOXGVHJRv0Fr-g-_Mg',	'2024-12-25 15:22:32.023005'),
('78unsnz5v7gwbvky6ougvjl70vgksrtv',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tXQdc:YWtboYHYgoPVYTa4Pm1Sm6g92QU8vLvlVOU0FiV0590',	'2025-01-27 20:02:16.280467'),
('7ss1yevsc36m1gererpe5slj56d93xt0',	'.eJxVjEEOwiAQRe_C2pAyCAwu3XsGMsAgVUOT0q6Md7dNutDtf-_9twi0LjWsnecwZnERTpx-t0jpyW0H-UHtPsk0tWUeo9wVedAub1Pm1_Vw_w4q9brVmov10SADWyo6GXQ6qjMiIxkH2iscNNAmOWt9yq4wJPBWDYg6gxOfL9mINxQ:1t5hhk:F32nKn8KQXdXcifDLhh2pcMnfaNpJJnVV4TDQqYURog',	'2024-11-12 08:35:56.420493'),
('7y2sxr7est2r6c4es7qrley46d1xr0jv',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t5g1R:Q6UFVZpHltr23dCUF4i5gNpULfCh34--9ZhURBpXvc0',	'2024-11-12 06:48:09.768245'),
('8sfhpb4lytlzb7tpr1m8ujpnx9am19qn',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t66zx:wYJXpq9rGMF__afNwXhugvVE3z-nikc_EInwMh9OP10',	'2024-11-13 11:36:25.696739'),
('8v30luyy7zwf7k0k6qx23utfaua5myg5',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1spqB4:dNK3OL_lFe9wHfiOYR8K_oEDfHnPPlqateJGuNcq358',	'2024-09-29 14:24:38.534849'),
('8yionmduaikukvqeyskv47kj27qzsfww',	'.eJxVjEEOwiAQRe_C2hChUMCle89AhhlGqgaS0q6Md7dNutDtf-_9t4iwLiWuPc9xInER-ixOv2MCfOa6E3pAvTeJrS7zlOSuyIN2eWuUX9fD_Tso0MtWIwZLjOy8Sc6RYcOBx5xNsoNTikOipBxmM4AJoEGrwY-OA-Fmk_Xi8wUzwjjq:1tloab:dFb80tbAsSC1khEA9Q2d6Y4dyJn2BIrfFN1PbTsbA9A',	'2025-03-08 12:26:37.188488'),
('9nqekwpu6zwn2fo215vhgirkyu9w2mh8',	'.eJxVjEEOwiAQRe_C2pDCDKW4dO8ZyACDVA0kpV0Z765NutDtf-_9l_C0rcVvnRc_J3EW2orT7xgoPrjuJN2p3pqMra7LHOSuyIN2eW2Jn5fD_Tso1Mu3toyKMGtUJkNmAEN5AgcMmIjjYJSy46iArLJRu4x6Mo4xAMeIJg3i_QH68Den:1tFr5h:8qpTatqmNOkZQ2Zb0TK1eDgAzrpQCADLW-x1hLlUm0I',	'2024-12-10 08:38:37.531064'),
('a41qx993nj8h5jdawwdbtam3ii5icqmw',	'.eJxVjDsOwjAQBe_iGlnxdw0lPWewdr02DiBHipMKcXdkKQW0b2beW0Tctxr3ntc4s7gILU6_G2F65jYAP7DdF5mWtq0zyaHIg3Z5Wzi_rof7d1Cx11GHxMX6wC55MEYVr_2krJ6ychYRDIEBADqT9RoKGKcKBMocgmEKID5fy4c3Lg:1t4iBH:jgmE6KhLKFJ6Xc6ySEU8jj8_SQRGeUHYOXy1OWdilLo',	'2024-11-09 14:54:19.740961'),
('awchc8ct8ib1mdk1hes11usccgmw3ghb',	'.eJxVjMEOwiAQBf-FsyHAAgWP3v0GArsgVQNJaU_Gf9cmPej1zcx7sRC3tYZt5CXMxM5MKnb6HVPER247oXtst86xt3WZE98VftDBr53y83K4fwc1jvqtQSsdXREYJ5ELApIoptgJsiBnfDFegUugpCEtndEANtsivZKoKEnN3h8AtTdw:1teJvo:sSF2K31ueprpMU7gI4fyM4XgF9jvc11H6CcHefDctWs',	'2025-02-15 20:17:32.172660'),
('ba01oxyhadpuv310g6dywhcmuvephcxb',	'.eJxVjEEOwiAQRe_C2pAhU4G6dO8ZyDADUjWQlHbVeHdt0oVu_3vvbyrQupSw9jSHSdRFGVSn3zESP1PdiTyo3pvmVpd5inpX9EG7vjVJr-vh_h0U6uVbA7EwoCBYZ7MhGfIolLIbkjEZPFqOZyHxYNGLEINhB84QIo_JDer9ASi3OK4:1t5tH6:kUSVbnDnntmO8JR4okUNUntm7tNnJg4aVk8LtLd7kzU',	'2024-11-12 20:57:12.364897'),
('c0qsq92f4gvi7isrxqjix0ovbvws7aoy',	'.eJxVjDkOwjAUBe_iGlnesDElfc5g_Q0cQI4UJxXi7hApBbRvZt5LFViXWtYucxlZnZWN6vA7ItBD2kb4Du02aZraMo-oN0XvtOthYnledvfvoEKv3xqNOArChCiYGU4iyXobU0ZE8Nl5iQTGBpsxWYnAxrjMiY4U6Bqien8AQjw5FA:1tD83A:9ZgvVY8DtXkyNhj6bmnOwAWlZZRrm66MuGPL80g1c1w',	'2024-12-02 20:08:44.346966'),
('cw72jw8dlwgin71i0sy5uzheh0ugblrd',	'.eJxVjEEOwiAQRe_C2hChUMCle89AhhlGqgaS0q6Md7dNutDtf-_9t4iwLiWuPc9xInER-ixOv2MCfOa6E3pAvTeJrS7zlOSuyIN2eWuUX9fD_Tso0MtWIwZLjOy8Sc6RYcOBx5xNsoNTikOipBxmM4AJoEGrwY-OA-Fmk_Xi8wUzwjjq:1tD64g:-jGtsXPtsiKyf6e26ceWa2WvMn15F6IGe3NnLcTi6cc',	'2024-12-02 18:02:10.840558'),
('edfx044n8fnpyx8yoraluov8fn428wmg',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tFBAp:pBnN69II7SC8pOTGTxr7WdKp29_fIQpP8Zc1GL4nQ9c',	'2024-12-08 11:53:07.037380'),
('eioul79qb1a977lh6r9uk6vmyj7sd7dn',	'.eJxVjDsOwjAQBe_iGlnxdw0lPWewdr02DiBHipMKcXdkKQW0b2beW0Tctxr3ntc4s7gILU6_G2F65jYAP7DdF5mWtq0zyaHIg3Z5Wzi_rof7d1Cx11GHxMX6wC55MEYVr_2krJ6ychYRDIEBADqT9RoKGKcKBMocgmEKID5fy4c3Lg:1spTN6:9PiGW9GVye5ytRGbbUCKmpTEjZot1rdSXE0Qr7xCyVE',	'2024-09-28 14:03:32.468761'),
('f9zwff92ob0wt4sk59ngs3a37lrlez74',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tiaJa:PIrQDludpS6ht-anHt-YuOScfvMS9qMcyHdlGBr08X0',	'2025-02-27 14:35:42.570810'),
('fb6ecfhqo2136818t6bj1dwq1cp20ayc',	'.eJxVjMEOwiAQBf-FsyHAAgWP3v0GArsgVQNJaU_Gf9cmPej1zcx7sRC3tYZt5CXMxM5MKnb6HVPER247oXtst86xt3WZE98VftDBr53y83K4fwc1jvqtQSsdXREYJ5ELApIoptgJsiBnfDFegUugpCEtndEANtsivZKoKEnN3h8AtTdw:1t9jHe:CKNGGb0TIfpYFm95bNV4BVNbkIkC4azMxBDMc5auPKQ',	'2024-11-23 11:05:38.710083'),
('fdnxsvykutvcz3yurrblbzxcndm1bs93',	'.eJxVjDsOwjAQBe_iGlnxJ_5Q0nMGa727xgHkSHFSIe4OkVJA-2bmvUSCba1p67ykicRZqCBOv2MGfHDbCd2h3WaJc1uXKctdkQft8joTPy-H-3dQoddvHXIB7wHJRxyUK0AmDhA16WhAITuLQXGwFEZTrM-oCRg0GjfqYHMR7w8pITjM:1tCHYQ:cO-lj6g4fDp0tsPmkpoLzRS5TYszzlo-cSQBoLZlfkA',	'2024-11-30 12:05:30.330370'),
('fihkg8jmhxe8cxyb3rmes1ehd3gayvxu',	'.eJxVjDsOwjAQBe_iGlnxdw0lPWewdr02DiBHipMKcXdkKQW0b2beW0Tctxr3ntc4s7gILU6_G2F65jYAP7DdF5mWtq0zyaHIg3Z5Wzi_rof7d1Cx11GHxMX6wC55MEYVr_2krJ6ychYRDIEBADqT9RoKGKcKBMocgmEKID5fy4c3Lg:1t54w7:T5NKOrpCdgiMsttIoUGLAVB2mNG1MDMdvPSWw1z5I88',	'2024-11-10 15:12:11.564912'),
('gbo40r214aw8pqhgtwfzgdzoxhvc6wno',	'.eJxVjMEOwiAQBf-FsyHAAgWP3v0GArsgVQNJaU_Gf9cmPej1zcx7sRC3tYZt5CXMxM5MKnb6HVPER247oXtst86xt3WZE98VftDBr53y83K4fwc1jvqtQSsdXREYJ5ELApIoptgJsiBnfDFegUugpCEtndEANtsivZKoKEnN3h8AtTdw:1tck6I:oRKOIqyDBE9NdS67slnvmBKRkOKizMgtwkDAI9Jo6Hg',	'2025-02-11 11:49:50.347069'),
('gjrrm50zmde8paz2jv0qzbus6ze4cngf',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tDTVb:oQ6hAOJu-MWfD_znbgZspnxrRZm3vWJ7QUQi7BIIEIY',	'2024-12-03 19:03:31.623430'),
('gn3z5arucao507vtffgz1osooxmegzca',	'.eJxVjEEOwiAQRe_C2pDCDKW4dO8ZyACDVA0kpV0Z765NutDtf-_9l_C0rcVvnRc_J3EW2orT7xgoPrjuJN2p3pqMra7LHOSuyIN2eW2Jn5fD_Tso1Mu3toyKMGtUJkNmAEN5AgcMmIjjYJSy46iArLJRu4x6Mo4xAMeIJg3i_QH68Den:1tTmhI:EWyVIeiwBglI-nKs4LllsZsjtxd6adD2I9vxKEZH7pM',	'2025-01-17 18:47:00.515932'),
('gvpavzuii15x4sgfoi1wublljaqtwjmp',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t55Nu:XxLTLqaz9FFDNR9_iP26ebLF_7euP6YjJ8Dtu74Vb_g',	'2024-11-10 15:40:54.374734'),
('hp9wjyb9orltftrugzowkbff3vorzkhn',	'.eJxVjEEOwiAQRe_C2pAyCAwu3XsGMsAgVUOT0q6Md7dNutDtf-_9twi0LjWsnecwZnERTpx-t0jpyW0H-UHtPsk0tWUeo9wVedAub1Pm1_Vw_w4q9brVmov10SADWyo6GXQ6qjMiIxkH2iscNNAmOWt9yq4wJPBWDYg6gxOfL9mINxQ:1tBzp6:DCjQ02oX9zhXqrlUpv3p4Bkr3Y9kCiMhyiqITQku6MA',	'2024-11-29 17:09:32.647161'),
('i1n6gfai9qmdhiqaf1y5dgfrm68zmu0p',	'.eJxVjDEOwjAMRe-SGUWpQ4rLyM4ZIie2SQGlUtNOiLtDpQ6w_vfef5lI61Li2mSOI5uz6c3hd0uUH1I3wHeqt8nmqS7zmOym2J02e51Ynpfd_Tso1Mq3VgBhyuAYehmUkemYT8KMnkNygRyR7wQ1CzlU9C4Bgg6owXcQgnl_AB9oOL4:1sqCs0:m_s2N_w8zRGmEioo0EIhZzn_Z9Wy1LDrBOrenPl-EU0',	'2024-09-30 14:38:28.689073'),
('if2vqjrhkouj88pvo2tq06xkiepy97z1',	'.eJxVjEEOwiAQRe_C2hAGwUGX7nsGMjOAVA1NSrsy3l2bdKHb_977LxVpXWpce57jmNRFHUEdfkcmeeS2kXSndpu0TG2ZR9abonfa9TCl_Lzu7t9BpV6_tRSx58BMIYC3SaxYNI4IiZHQmZLEAYAPPgeyZBJaPoEpgYUQwav3BxySOEk:1tWeeO:E6EZXnHwfmcftaG8age0Nwvwccpm9jBkMv-kAza2Jbg',	'2025-01-25 16:47:52.496943'),
('jrczze6osh0fygjybu76xzn71ec04dll',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tFg2c:8w6RAfvFK-oSXKRrPg4Rng_h_aH6sCsQqOYlmUbX75I',	'2024-12-09 20:50:42.854163'),
('jwu15bqxfrcqbpqyup19lyf9o4q8k7ri',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tJ7hE:3-tHRXLSD5BBHa-WsekI2sMiunVnO-u97MXjk7nM4eE',	'2024-12-19 08:58:52.545199'),
('k4hs27vcj2plij9jsyxri6j5lsliwozz',	'.eJxVjM0OwiAQhN-FsyEtID8evfsMZJddpGogKe3J-O62SQ96m8z3zbxFhHUpce08x4nERaggTr8lQnpy3Qk9oN6bTK0u84RyV-RBu7w14tf1cP8OCvSyrTEorTxZTGMCY00mQ55t0kQOfN7CiOfszEAJtBsCasvOW_bKaCaN4vMFJMc4pQ:1tNv93:t3B3sdnG6V5f5QsmyBOsmiSALSRgCo5UgpFJnTLnPzs',	'2025-01-01 14:35:25.560494'),
('kar60tqw8of6025i90tpufasf1ebwcbh',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tFYYe:6nAl27QB0C4vNz2c65QOk-RTjl6sALlM5z40ysryysg',	'2024-12-09 12:51:16.044541'),
('kcifvij2g5tg1imx5wh1wtj2mardd9pr',	'.eJxVjDsOwjAQBe_iGln-rbOmpM8ZLK8_OIAcKU4qxN1JpBTQvpl5b-bDtla_9bz4KbErU5ZdfkcK8ZnbQdIjtPvM49zWZSJ-KPyknY9zyq_b6f4d1NDrXtsoDAzkrEZbsgEUAEggiKIRgEaiKyiKHqRWijRGTFED7FZ2qJJkny_WQzab:1tFpDZ:1FaTxLoqhY9vFp7M0wdGEhFSO0rMx54Ip8gGzF_aWcI',	'2024-12-10 06:38:37.290797'),
('kg2em3p1rll6zcteqls01yt3qks8kyq0',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tMV9c:cujVZKv72qfMMb8oXOcyJhD1yLw-OydqYZ1x92AQqrU',	'2024-12-28 16:38:08.519191'),
('kkx9li6fk0ovqkv4cbwhe7i6ie8147f0',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tEkZH:sjHSPUxWvbuhJ9pg2iKAHEFOD70d1AxwMigLaona7hU',	'2024-12-07 07:28:35.736944'),
('lc0vfcf2xzau32srm8wtv8omlt9vjxnb',	'.eJxVjEEOwiAQRe_C2hChUMCle89AhhlGqgaS0q6Md7dNutDtf-_9t4iwLiWuPc9xInER-ixOv2MCfOa6E3pAvTeJrS7zlOSuyIN2eWuUX9fD_Tso0MtWIwZLjOy8Sc6RYcOBx5xNsoNTikOipBxmM4AJoEGrwY-OA-Fmk_Xi8wUzwjjq:1tHHKq:atFlgTFwl5E5qDHO1ivOawrZqKwGceC1_gax6yKPAKQ',	'2024-12-14 06:52:08.306368'),
('lkeyqovkwegla1o4wgyj01vn5mjz0v6v',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tGkKW:la49NsEjE50xJCc7UpUP4dECT_mdgB539WygOZBjPDc',	'2024-12-12 19:37:36.868167'),
('lqzuk0hgmew7894xvubye7les0hbfi8w',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tFYaH:fzxtcSo6w6Y6kBjtF2JUKoW0Y5KmjKiTi6vnsHxsfUc',	'2024-12-09 12:52:57.187933'),
('lr5gw1b52314d0f2n0mto30cotuyq7jz',	'.eJxVjEEOwiAQRe_C2pAyCAwu3XsGMsAgVUOT0q6Md7dNutDtf-_9twi0LjWsnecwZnERTpx-t0jpyW0H-UHtPsk0tWUeo9wVedAub1Pm1_Vw_w4q9brVmov10SADWyo6GXQ6qjMiIxkH2iscNNAmOWt9yq4wJPBWDYg6gxOfL9mINxQ:1swJ5T:v19bI4kLpLChMReOWiMRB_SgUzZzRjwFGWxM70W-xys',	'2024-10-17 10:29:35.926071'),
('lvfw97qbtfwzrnn6x35trvidwg2ugujv',	'.eJxVjEEOgjAQRe_StWkqpR3q0j1nIDP9g6AGEgor492VhIVu_3vvv0zH2zp0W9GlG2Euxgdz-h2F80OnneDO0222eZ7WZRS7K_agxbYz9Hk93L-DgcvwrYVyPtdNDYACPGJI3FOEwkWKLEmCrzxx0t4pk0pCn-CqhhQcOZj3By9xOUE:1tg52I:L5PmgA-3abgRnqXxKzfWm5CpKZBwPVlilXZ-v5eVoqk',	'2025-02-20 16:47:30.210539'),
('mzf53otsjacxcgygk4uisut9l95852on',	'.eJxVjMEOwiAQBf-FsyHAAgWP3v0GArsgVQNJaU_Gf9cmPej1zcx7sRC3tYZt5CXMxM5MKnb6HVPER247oXtst86xt3WZE98VftDBr53y83K4fwc1jvqtQSsdXREYJ5ELApIoptgJsiBnfDFegUugpCEtndEANtsivZKoKEnN3h8AtTdw:1tLuNR:Vb9F-4f6e2zcKW-WeYfnjWTF3bLuVG29Ta5wWTN5Ffg',	'2024-12-27 01:21:57.037786'),
('n2xdq2do1tk9dkz50zxsv23lff23xcla',	'.eJxVjDsOwjAQBe_iGlnxdw0lPWewdr02DiBHipMKcXdkKQW0b2beW0Tctxr3ntc4s7gILU6_G2F65jYAP7DdF5mWtq0zyaHIg3Z5Wzi_rof7d1Cx11GHxMX6wC55MEYVr_2krJ6ychYRDIEBADqT9RoKGKcKBMocgmEKID5fy4c3Lg:1stAm5:cRPmvK9AQ_Sdys5qpl9CT7d0zEv4URcSd6-_l_y-jYQ',	'2024-10-08 19:00:37.965907'),
('n88tl2gxcc8nqxzskictdur68903xwo6',	'.eJxVjEEOwiAQRe_C2pDCDKW4dO8ZyACDVA0kpV0Z765NutDtf-_9l_C0rcVvnRc_J3EW2orT7xgoPrjuJN2p3pqMra7LHOSuyIN2eW2Jn5fD_Tso1Mu3toyKMGtUJkNmAEN5AgcMmIjjYJSy46iArLJRu4x6Mo4xAMeIJg3i_QH68Den:1tZxfT:8CWQQDD-xiT69043PGSybx7MX9yJE5tQMwiHrxCrGcg',	'2025-02-03 19:42:39.615809'),
('neg6gr73tpgvvof5zb7thr9yhomlcm7d',	'.eJxVjDsOwjAQBe_iGln-Y1PS5wzW7nqNAyiR4qRC3B0ipYD2zcx7iQzb2vLWecljERdhojj9jgj04Gkn5Q7TbZY0T-syotwVedAuh7nw83q4fwcNevvWSqlzoui0p5CogiUMLmin2LMn44OygMlZIFdiZZMwVOu14uoRCqN4fwD3jThd:1tGLOO:SuEOWnf948qI1HZyMlTgsiDLwC-nAsh15upn8YOkZLw',	'2024-12-11 16:59:56.231263'),
('o6hjp7b76221y63g1kubvok69lubp5sy',	'.eJxVjMsOwiAQRf-FtSE8hg64dO83kAGmUjU0Ke3K-O_apAvd3nPOfYlI21rj1nmJUxFnYa04_Y6J8oPbTsqd2m2WeW7rMiW5K_KgXV7nws_L4f4dVOr1W3scNI42sTJIrAnBh-QwJwjIXhdgUMbaYlSmpAOYDMX4QWmn3agIxfsD8oo3Ow:1taOu0:NxkrzkSvlatlZAKsaxS4VGpmVY-9pK9M8ii5XKnk22k',	'2025-02-05 00:47:28.452268'),
('obukcwbk597emqzedh5t098glpprcedv',	'.eJxVjEEOwiAQRe_C2hChUMCle89AhhlGqgaS0q6Md7dNutDtf-_9t4iwLiWuPc9xInER-ixOv2MCfOa6E3pAvTeJrS7zlOSuyIN2eWuUX9fD_Tso0MtWIwZLjOy8Sc6RYcOBx5xNsoNTikOipBxmM4AJoEGrwY-OA-Fmk_Xi8wUzwjjq:1tMQXj:DN7DPiEpuDoYs2J1dnubx3-EMWSlgsvRPE8gad4W3xA',	'2024-12-28 11:42:43.739361'),
('p31w5gpixkdqumeth7rj3e0t3zzvwi3c',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tloQ1:JmZuY2QIYv9Kjdzsbab2p92K7FVS6iRxffn-2BQvzTQ',	'2025-03-08 12:15:41.900415'),
('p5uuirwh4j8z9envxgtjkm06sn660cst',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t6odr:BmYkkWVd0lTAM-2H9VjHGlDDl8lIFBxwFiLQf44bXrk',	'2024-11-15 10:12:31.047553'),
('pl5ggmt8xucahfu7o4iapqeoj5xsbkbv',	'.eJxVjMEOwiAQBf-FsyHAAgWP3v0GArsgVQNJaU_Gf9cmPej1zcx7sRC3tYZt5CXMxM5MKnb6HVPER247oXtst86xt3WZE98VftDBr53y83K4fwc1jvqtQSsdXREYJ5ELApIoptgJsiBnfDFegUugpCEtndEANtsivZKoKEnN3h8AtTdw:1t5qih:8lldcRaV6vB-p76emPGxBDa34-5PC7TV3uB-pgEB7fk',	'2024-11-12 18:13:31.489279'),
('q7630c04sm4jfe6grz833j1iahrok7n9',	'.eJxVjMsOwiAQRf-FtSHIAC0u3fcbyHRmkKqBpI-V8d-1SRe6veec-1IJt7WkbZE5Tawuyp7V6XcckR5Sd8J3rLemqdV1nka9K_qgix4ay_N6uH8HBZfyrdGieId9tBAsMIYsElx0GCBT7x15YiTInXGGoTOM4GMAtkwcZUT1_gAUMzi_:1tEOyg:0ZZ5ziXo2CdPtE0NuA8AH-DhmsMTVlsF6OOaj7HAkDo',	'2024-12-06 08:25:22.316026'),
('qd9t5e6xiyede8bbro3w9tb8hlvh3xod',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tFpEV:786BtgbIj82i3WolmNG52KR7WJfnfb_EVn1Nv7RVU1I',	'2024-12-10 06:39:35.781425'),
('qg5sc0zvlsea3ao1csh98ijv8l1r3ljg',	'.eJxVjDkOwjAUBe_iGlnfuz8lfc5gecUBZEtxUiHuTiKlgPbNzHsT57e1um3kxc2JXAlDcvkdg4_P3A6SHr7dO429rcsc6KHQkw469ZRft9P9O6h-1L0uqLOKqIMFRCmK4iIFWbjmRakYVNIghbGIhrPIOLO74I3QwAqAAEk-X-mxNmI:1tCjZq:cqkvADsFWzUE--HAf-ynR8E0Iz3HdjMLNljUBgjyXcA',	'2024-12-01 18:00:50.095957'),
('qjv4go5t75vfs14zvel3p3ng4slirip4',	'.eJxVjDsOwjAQBe_iGlnxD3sp6XMGa9fr4ACypTipEHeHSCmgfTPzXiLitpa49bzEmcVFaCtOvyNheuS6E75jvTWZWl2XmeSuyIN2OTbOz-vh_h0U7OVbn7Xi7E1CqzEAKAfMQ_CeWXEgnRJAmLxVyg8MQM44C0QuGTYTaGXE-wP8DjeQ:1tFB8P:6m7R4ABcGeQ9UlEh3jYITOxdIvr57UiI_iRUkbOtme8',	'2024-12-08 11:50:37.783100'),
('rhznlqtr2v3tk1jw9e2k4wpuuwwdf6og',	'.eJxVjDEOwjAMRe-SGUWpQ4rLyM4ZIie2SQGlUtNOiLtDpQ6w_vfef5lI61Li2mSOI5uz6c3hd0uUH1I3wHeqt8nmqS7zmOym2J02e51Ynpfd_Tso1Mq3VgBhyuAYehmUkemYT8KMnkNygRyR7wQ1CzlU9C4Bgg6owXcQgnl_AB9oOL4:1sqzmx:xxSmwz9I-v5N7ynu0_Ah8raaRv060uV57U5KxGI9z-0',	'2024-10-02 18:52:31.749145'),
('rpg6wovzvks44q6bblsntztvyyaljv0e',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tJ7gJ:X7GAZcFbiXcaSnJWnDzacFW5V4EV986ukYY4-3f4vFU',	'2024-12-19 08:57:55.409601'),
('s05ygvwim2o38iz31iyptjb6d6y5n79m',	'.eJxVjDsOwjAQBe_iGlnxdw0lPWewdr02DiBHipMKcXdkKQW0b2beW0Tctxr3ntc4s7gILU6_G2F65jYAP7DdF5mWtq0zyaHIg3Z5Wzi_rof7d1Cx11GHxMX6wC55MEYVr_2krJ6ychYRDIEBADqT9RoKGKcKBMocgmEKID5fy4c3Lg:1spLsY:r6lJ9GviOwAlWY87e6Mq_SuX_jHLrm6tDS2XNDs4Zsw',	'2024-09-28 06:03:30.480409'),
('tsbt1m8kti76li5c8t9pvtiktb78pz57',	'.eJxVjDkOwjAUBe_iGlnesDElfc5g_Q0cQI4UJxXi7hApBbRvZt5LFViXWtYucxlZnZWN6vA7ItBD2kb4Du02aZraMo-oN0XvtOthYnledvfvoEKv3xqNOArChCiYGU4iyXobU0ZE8Nl5iQTGBpsxWYnAxrjMiY4U6Bqien8AQjw5FA:1t6DAw:uQG10tZ5fiBsXf0LaiKxHgImiczKz3gly0521l-0aus',	'2024-11-13 18:12:10.721431'),
('tv404njacbem5kte1190f2rfvdyaz39c',	'.eJxVjMEOwiAQRP-FsyEUWAWP3vsNZLu7laqhSWlPxn-XJj3oaZJ5b-atEm5rTluVJU2srsp5dfotB6SnlJ3wA8t91jSXdZkGvSv6oFX3M8vrdrh_BxlrbmtrIBKwYQ6W2LFvQYDBwxmMjWhCFHQ2joKXFo6iD6N0iGjBsXTq8wUAfDgF:1tg51j:7_OGUB21a8eScC_elR9XuI0-fVUOX0F5n6m0OKK1Urs',	'2025-02-20 16:46:55.259475'),
('tylv6sfmf91509g4bge4d9uth7cd0ovz',	'.eJxVjEEOwiAQRe_C2pAhU4G6dO8ZyDADUjWQlHbVeHdt0oVu_3vvbyrQupSw9jSHSdRFGVSn3zESP1PdiTyo3pvmVpd5inpX9EG7vjVJr-vh_h0U6uVbA7EwoCBYZ7MhGfIolLIbkjEZPFqOZyHxYNGLEINhB84QIo_JDer9ASi3OK4:1tFKDD:cCoALe-czzyz69IhpuIfCVxm6RKbSzCXnivlAivRmW0',	'2024-12-08 21:32:11.448883'),
('u28c3vjpagfhk87hub1xqrra3b68fiif',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t5ftv:1290E2Aeen5lXoHVETCuROGJRLJiRDkOkvIgU3s8qi8',	'2024-11-12 06:40:23.819395'),
('udig9fldug5img25tazqlm4k6cp0iik3',	'.eJxVjDkOwjAUBe_iGlnesDElfc5g_Q0cQI4UJxXi7hApBbRvZt5LFViXWtYucxlZnZWN6vA7ItBD2kb4Du02aZraMo-oN0XvtOthYnledvfvoEKv3xqNOArChCiYGU4iyXobU0ZE8Nl5iQTGBpsxWYnAxrjMiY4U6Bqien8AQjw5FA:1tatIJ:ZUmULgzcZqWyR1RjKumXxEsx3F_cHpHhPWxzbRzMfEQ',	'2025-02-06 09:14:35.414978'),
('v78xhsi61kjji181ycdxiatehvb0zezp',	'.eJxVjEEOwiAQRe_C2pDCDKW4dO8ZyACDVA0kpV0Z765NutDtf-_9l_C0rcVvnRc_J3EW2orT7xgoPrjuJN2p3pqMra7LHOSuyIN2eW2Jn5fD_Tso1Mu3toyKMGtUJkNmAEN5AgcMmIjjYJSy46iArLJRu4x6Mo4xAMeIJg3i_QH68Den:1tONbr:YimT9aZOTULulSEWcZeH4z7SpiuS5_hfzn_y4gtpII0',	'2025-01-02 20:59:03.683325'),
('w0ie29ci16yb4igdfsom6yzkrbd468k9',	'.eJxVjMsOwiAQRf-FtSHIAC0u3fcbyHRmkKqBpI-V8d-1SRe6veec-1IJt7WkbZE5Tawuyp7V6XcckR5Sd8J3rLemqdV1nka9K_qgix4ay_N6uH8HBZfyrdGieId9tBAsMIYsElx0GCBT7x15YiTInXGGoTOM4GMAtkwcZUT1_gAUMzi_:1tKEqf:0rZpJeBY_cT7Viw9REKTJalg6kMWhWfWsX5MyaOpbSc',	'2024-12-22 10:49:13.117526'),
('w5t0horrzo85ogmhv698df4k47kyii4a',	'.eJxVjMsOwiAQRf-FtSHIAC0u3fcbyHRmkKqBpI-V8d-1SRe6veec-1IJt7WkbZE5Tawuyp7V6XcckR5Sd8J3rLemqdV1nka9K_qgix4ay_N6uH8HBZfyrdGieId9tBAsMIYsElx0GCBT7x15YiTInXGGoTOM4GMAtkwcZUT1_gAUMzi_:1tGjWV:EnUoQQlzPTTb-TUyupSSe9hbJ2g3TeeNfiG9I3dyGMo',	'2024-12-12 18:45:55.482151'),
('wgnwgqyvipihslh0f336ddtflxlc583m',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tL751:04C2VExKKCur8d6-EuZy_Oi2LdH6U6SUKFuszAiRyo0',	'2024-12-24 20:43:39.793035'),
('wncj7aawpovl18sbmhxgwq39s46nhgmc',	'.eJxVjEEOwiAQRe_C2hChUMCle89AhhlGqgaS0q6Md7dNutDtf-_9t4iwLiWuPc9xInER-ixOv2MCfOa6E3pAvTeJrS7zlOSuyIN2eWuUX9fD_Tso0MtWIwZLjOy8Sc6RYcOBx5xNsoNTikOipBxmM4AJoEGrwY-OA-Fmk_Xi8wUzwjjq:1tL5pc:MW3ninabTsL7OLJCqSYJdMLeiBMZEYtEpfJvFdZXXDk',	'2024-12-24 19:23:40.664248'),
('xkueifl8txiuiowtspfic3diyc5xbjg0',	'.eJxVjDEOwjAMRe-SGUWpQ4rLyM4ZIie2SQGlUtNOiLtDpQ6w_vfef5lI61Li2mSOI5uz6c3hd0uUH1I3wHeqt8nmqS7zmOym2J02e51Ynpfd_Tso1Mq3VgBhyuAYehmUkemYT8KMnkNygRyR7wQ1CzlU9C4Bgg6owXcQgnl_AB9oOL4:1spTh2:r-6dknS7pvOfkXIDC_oQFTto_hpiIOibEXsDs3KBQ9w',	'2024-09-28 14:24:08.122448'),
('yot7rymwawczqa3ik863tjti8n2xw9kq',	'.eJxVjEEOwiAQRe_C2pApAxRcuvcMZBhAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hSuIsEMTpd4zEj9x2ku7UbrPkua3LFOWuyIN2eZ1Tfl4O9--gUq_fGpwtMSpdMPOAafSIULIrho3yDgePOgKjQ_IaQFmyrJNGYx2MBpjE-wPyUDcO:1tWedP:Pq2td2i1aq_pd7T9fUOtIrISbu4zKYEQTN8FDrkIszs',	'2025-01-25 16:46:51.524274'),
('ys9h9hrpfhrje6sckaqtranduvq2yx98',	'.eJxVjEEOwiAQRe_C2hChUMCle89AhhlGqgaS0q6Md7dNutDtf-_9t4iwLiWuPc9xInER-ixOv2MCfOa6E3pAvTeJrS7zlOSuyIN2eWuUX9fD_Tso0MtWIwZLjOy8Sc6RYcOBx5xNsoNTikOipBxmM4AJoEGrwY-OA-Fmk_Xi8wUzwjjq:1tMNOB:MLMPO7_xxslF0UCQgljsVn1r4ntxdIflNgDsCXye6J4',	'2024-12-28 08:20:39.402309'),
('zabriwdk6xz98p30eotppqxz8rjwqxgx',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1tQKMX:Q3BzjIo8tUCGnMXqrOZ4eH7pPFP2Tt7v6Ypm_-LqU6I',	'2025-01-08 05:55:17.022545'),
('zay5n1jtlsjbmxlabetaktdrrksikxe5',	'.eJxVjMsOwiAUBf-FtSEtUOC6dO83kPsAWzUlKe3K-O_apAvdnpk5L5VwW8e0tbykSdRZ9er0uxHyI887kDvOt6q5zusykd4VfdCmr1Xy83K4fwcjtvFbBykC5LJll7nEYZDOoaXMhkqMKAMDF4MQPHWmC70HJijRQrDABr16fwAYDTiq:1t6uZ3:s-g8e1UbarkZ9qELlTiEypLe1hyuIzLYAnOS3yH3YK8',	'2024-11-15 16:31:57.587917');

CREATE TABLE `django_summernote_attachment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `file` varchar(100) NOT NULL,
  `uploaded` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_activity_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_action` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL,
  `date_time` datetime(6) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `FDK_activity_log_user_id_a546678b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `FDK_activity_log_user_id_a546678b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_attachments` (
  `attachment_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_date` datetime(6) DEFAULT NULL,
  `task_id` int(11) NOT NULL,
  `uploaded_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`attachment_id`),
  KEY `FDK_attachments_task_id_6338ddb5_fk_FDK_tasks_task_id` (`task_id`),
  KEY `FDK_attachments_uploaded_by_97a04ef4_fk_FDK_users_user_id` (`uploaded_by`),
  CONSTRAINT `FDK_attachments_task_id_6338ddb5_fk_FDK_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `FDK_tasks` (`task_id`),
  CONSTRAINT `FDK_attachments_uploaded_by_97a04ef4_fk_FDK_users_user_id` FOREIGN KEY (`uploaded_by`) REFERENCES `FDK_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_categories` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `language` varchar(2) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  KEY `FDK_categories_project_id_24738d00_fk_FDK_projects_project_id` (`project_id`),
  CONSTRAINT `FDK_categories_project_id_24738d00_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_categories` (`category_id`, `name`, `description`, `language`, `project_id`) VALUES
(1,	'Frontend',	'Základní kategorie: Frontend',	NULL,	21),
(2,	'Backend',	'Základní kategorie: Backend',	NULL,	21),
(3,	'Database',	'Základní kategorie: Database',	NULL,	21),
(4,	'Frontend',	'Základní kategorie: Frontend',	NULL,	22),
(5,	'Backend',	'Základní kategorie: Backend',	NULL,	22),
(6,	'Database',	'Základní kategorie: Database',	NULL,	22),
(7,	'Frontend',	'Základní kategorie: Frontend',	NULL,	23),
(8,	'Backend',	'Základní kategorie: Backend',	NULL,	23),
(9,	'Database',	'Základní kategorie: Database',	NULL,	23),
(10,	'Front',	'Základní kategorie: Frontend',	NULL,	24),
(11,	'Backend',	'Základní kategorie: Backend',	NULL,	24),
(13,	'Frontend',	'Základní kategorie: Frontend',	NULL,	25),
(14,	'Backend',	'Základní kategorie: Backend',	NULL,	25),
(15,	'Database',	'Základní kategorie: Database',	NULL,	25),
(16,	'Frontend',	'Základní kategorie: Frontend',	NULL,	26),
(17,	'Backend',	'Základní kategorie: Backend',	NULL,	26),
(18,	'Database',	'Základní kategorie: Database',	NULL,	26),
(19,	'Frontend',	'Základní kategorie: Frontend',	NULL,	27),
(20,	'Backend',	'Základní kategorie: Backend',	NULL,	27),
(21,	'Database',	'Základní kategorie: Database',	NULL,	27),
(22,	'Frontend',	'Základní kategorie: Frontend',	NULL,	28),
(23,	'Backend',	'Základní kategorie: Backend',	NULL,	28),
(24,	'Database',	'Základní kategorie: Database',	NULL,	28),
(25,	'Frontend',	'Základní kategorie: Frontend',	NULL,	29),
(26,	'Backend',	'Základní kategorie: Backend',	NULL,	29),
(27,	'Database',	'Základní kategorie: Database',	NULL,	29),
(28,	'Frontend',	'Základní kategorie: Frontend',	NULL,	30),
(29,	'Backend',	'Základní kategorie: Backend',	NULL,	30),
(30,	'Database',	'Základní kategorie: Database',	NULL,	30),
(31,	'Frontend',	'Základní kategorie: Frontend',	NULL,	31),
(32,	'Backend',	'Základní kategorie: Backend',	NULL,	31),
(33,	'Database',	'Základní kategorie: Database',	NULL,	31),
(34,	'Frontend',	'Základní kategorie: Frontend',	NULL,	32),
(35,	'Backend',	'Základní kategorie: Backend',	NULL,	32),
(36,	'Database',	'Základní kategorie: Database',	NULL,	32),
(37,	'Frontend',	'Základní kategorie: Frontend',	NULL,	33),
(38,	'Backend',	'Základní kategorie: Backend',	NULL,	33),
(39,	'Database',	'Základní kategorie: Database',	NULL,	33),
(40,	'Čtvrtá kategorie',	'ahoj',	NULL,	24),
(42,	'Testování',	'',	NULL,	18),
(43,	'Frontend',	'',	NULL,	18),
(44,	'Backend',	'',	NULL,	18),
(45,	'test',	'',	NULL,	2),
(47,	'Grafika',	'Grafika',	NULL,	34),
(48,	'Vzdělávání',	'Vzdělávací materiálu',	NULL,	34),
(49,	'Hry',	'Zábava - bludiště',	NULL,	34),
(50,	'Frontend',	'Základní kategorie: Frontend',	NULL,	35),
(51,	'Backend',	'Základní kategorie: Backend',	NULL,	35),
(52,	'Database',	'Základní kategorie: Database',	NULL,	35),
(53,	'Frontend',	'Základní kategorie: Frontend',	NULL,	36),
(54,	'Backend',	'Základní kategorie: Backend',	NULL,	36),
(55,	'Database',	'Základní kategorie: Database',	NULL,	36),
(56,	'Frontend',	'Základní kategorie: Frontend',	NULL,	37),
(57,	'Backend',	'Základní kategorie: Backend',	NULL,	37),
(58,	'Database',	'Základní kategorie: Database',	NULL,	37),
(59,	'3D artefakty',	'3D',	NULL,	38),
(60,	'Technická podpora',	'Základní kategorie: Backend',	NULL,	38),
(61,	'Zdroje dat a informací',	'Základní kategorie: Database',	NULL,	38),
(62,	'Web',	'',	NULL,	34),
(63,	'Aktivity',	'Pohybové hry',	NULL,	34),
(64,	'Proces a metodika',	'',	NULL,	34),
(65,	'Frontend',	'Základní kategorie: Frontend',	NULL,	39),
(66,	'Backend',	'Základní kategorie: Backend',	NULL,	39),
(67,	'Database',	'Základní kategorie: Database',	NULL,	39),
(68,	'Frontend',	'Základní kategorie: Frontend',	NULL,	40),
(69,	'Backend',	'Základní kategorie: Backend',	NULL,	40),
(70,	'Database',	'Základní kategorie: Database',	NULL,	40),
(71,	'Komunikace a spolupráce',	'',	NULL,	38),
(72,	'Frontend',	'Základní kategorie: Frontend',	NULL,	41),
(73,	'Backend',	'Základní kategorie: Backend',	NULL,	41),
(74,	'Database',	'Základní kategorie: Database',	NULL,	41),
(75,	'Mobile App',	'',	NULL,	37);

CREATE TABLE `FDK_comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` longtext DEFAULT NULL,
  `posted` datetime(6) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `task_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `FDK_comments_project_id_44f27614_fk_FDK_projects_project_id` (`project_id`),
  KEY `FDK_comments_task_id_09a220a7_fk_FDK_tasks_task_id` (`task_id`),
  KEY `FDK_comments_user_id_919a906c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `FDK_comments_project_id_44f27614_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`),
  CONSTRAINT `FDK_comments_task_id_09a220a7_fk_FDK_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `FDK_tasks` (`task_id`),
  CONSTRAINT `FDK_comments_user_id_919a906c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_comments` (`comment_id`, `comment`, `posted`, `project_id`, `task_id`, `user_id`) VALUES
(1,	'test',	'2024-10-31 06:15:15.620362',	18,	46,	1),
(2,	'test2',	'2024-10-31 06:15:27.715848',	18,	46,	1),
(3,	'Podle čeho filtrovat? Možná kategorie?',	'2024-10-31 20:14:30.101673',	18,	29,	1),
(4,	'Já bych dala podle jména čí je úkol, pak podle priority a v celkovém přehledu i podle projektu a deadline',	'2024-11-15 17:12:09.622006',	18,	29,	7),
(5,	'hotovo',	'2024-11-30 22:29:50.277484',	37,	57,	1);

CREATE TABLE `FDK_company` (
  `company_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `street` varchar(128) NOT NULL,
  `street_number` varchar(10) NOT NULL,
  `city` varchar(128) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `state` varchar(128) NOT NULL,
  `ico` varchar(20) NOT NULL,
  `dic` varchar(20) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `is_vat_payer` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`company_id`),
  UNIQUE KEY `ico` (`ico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_company_users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `FDK_company_users_company_id_user_id_56ae9902_uniq` (`company_id`,`user_id`),
  KEY `FDK_company_users_user_id_b5967131_fk_auth_user_id` (`user_id`),
  CONSTRAINT `FDK_company_users_company_id_bd18b2cb_fk_FDK_company_company_id` FOREIGN KEY (`company_id`) REFERENCES `FDK_company` (`company_id`),
  CONSTRAINT `FDK_company_users_user_id_b5967131_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_contacts` (
  `contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `added_on` datetime(6) NOT NULL,
  `last_contacted` datetime(6) DEFAULT NULL,
  `is_private` tinyint(1) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`contact_id`),
  KEY `FDK_contacts_account_id_94544242_fk_auth_user_id` (`account_id`),
  KEY `FDK_contacts_project_id_acca62ab_fk_FDK_projects_project_id` (`project_id`),
  CONSTRAINT `FDK_contacts_account_id_94544242_fk_auth_user_id` FOREIGN KEY (`account_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `FDK_contacts_project_id_acca62ab_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_contacts` (`contact_id`, `first_name`, `last_name`, `phone`, `email`, `company`, `description`, `added_on`, `last_contacted`, `is_private`, `account_id`, `project_id`) VALUES
(1,	'Martin',	'Kučera',	'776106378',	'martin@div.cz',	NULL,	'1 2 3',	'2024-09-13 16:34:31.572762',	NULL,	0,	NULL,	NULL),
(2,	'z.s.',	'eKultura',	'776106378',	NULL,	NULL,	'',	'2024-09-13 16:34:45.472104',	NULL,	0,	NULL,	NULL),
(3,	'Martin',	'Kučera',	'776106378',	'martin@div.cz',	NULL,	'',	'2024-09-13 16:34:51.826299',	NULL,	0,	NULL,	NULL),
(4,	'Veronika',	'Kučerová',	NULL,	NULL,	NULL,	'',	'2024-09-13 16:42:04.921387',	NULL,	0,	NULL,	NULL),
(5,	'Veronika',	'Kučerová',	NULL,	NULL,	NULL,	'',	'2024-09-13 17:18:46.158869',	NULL,	0,	NULL,	NULL),
(13,	'Pavel',	'Kucera',	'5566',	NULL,	NULL,	'',	'2024-09-14 14:04:40.141858',	NULL,	1,	2,	16),
(14,	'Pavel',	'Kucera',	NULL,	NULL,	NULL,	'',	'2024-09-14 14:04:48.951910',	NULL,	0,	2,	NULL),
(18,	'TestLenka1',	'Test',	'733711758',	NULL,	NULL,	'xxx',	'2024-09-24 19:03:48.850131',	NULL,	1,	7,	NULL),
(19,	'Martin',	'Kučera',	'776106378',	'media@ekultura.eu',	'eKultura, z.s.',	's',	'2024-10-27 20:39:20.438614',	NULL,	0,	1,	NULL),
(20,	'Veronika',	'Kučerová',	NULL,	NULL,	NULL,	'',	'2024-10-27 21:48:23.276158',	NULL,	0,	1,	NULL),
(21,	'Test',	NULL,	NULL,	NULL,	'Bb',	'',	'2024-10-27 22:14:34.664819',	NULL,	0,	1,	18),
(22,	'Martin',	'Kučera',	'776106378',	'media@ekultura.eu',	'eKultura, z.s.',	'',	'2024-10-28 16:53:26.356762',	NULL,	1,	10,	35),
(23,	'Pavel',	NULL,	NULL,	NULL,	NULL,	'',	'2024-10-28 17:00:47.100300',	NULL,	1,	10,	35),
(24,	'Kritika',	'Sethi',	NULL,	'kritika-sethi@wevaad.com',	'Wevaad',	'Can I translate your article?\r\nhttps://www.policycircle.org/policy/arbitration-mediation-disputes/)',	'2024-10-28 17:04:17.171360',	NULL,	0,	1,	36),
(25,	'wevaad',	NULL,	NULL,	'contact@wevaad.com',	NULL,	'e-mail: Can I translate your article?',	'2024-10-28 17:04:52.578499',	NULL,	1,	1,	36),
(26,	'Policycircle.org',	NULL,	NULL,	'outreach@policycircle.org',	NULL,	'Can I translate your article?',	'2024-10-28 17:05:19.098417',	NULL,	1,	1,	36),
(27,	'NAS',	NULL,	NULL,	'nas@circ.in',	NULL,	'Can I translate your article?',	'2024-10-28 17:05:43.031300',	NULL,	1,	1,	36),
(28,	'N.Gould',	NULL,	NULL,	'ngould@fenwickelliott.com',	NULL,	'Request for Permission to Translate and Publish \"Mediation Guide - The Basics\"',	'2024-10-28 17:06:12.322952',	NULL,	1,	1,	36),
(29,	'PON',	NULL,	NULL,	'pon@law.harvard.edu',	NULL,	'Request for Permission to Translate and Publish \"The Program on Negotiation\"',	'2024-10-28 17:06:32.709000',	NULL,	1,	1,	36),
(31,	'Martin',	'Kučera',	'776106378',	'martin1.kucera@t-mobile.cz',	'T-Mobile',	'',	'2024-12-18 14:39:37.833934',	NULL,	0,	29,	41),
(32,	'maklerský',	'projekt',	NULL,	NULL,	NULL,	'',	'2024-12-18 14:40:07.342426',	NULL,	1,	29,	41);

CREATE TABLE `FDK_contract` (
  `contract_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `document` varchar(100) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`contract_id`),
  KEY `fdk_cz_contract_project_id_708876b1_fk_FDK_projects_project_id` (`project_id`),
  CONSTRAINT `fdk_cz_contract_project_id_708876b1_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_documents` (
  `document_id` int(11) NOT NULL AUTO_INCREMENT,
  `document_type` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `project_id` int(11) NOT NULL,
  `uploaded_by` int(11) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  PRIMARY KEY (`document_id`),
  KEY `FDK_documents_project_id_3a254b12_fk_FDK_projects_project_id` (`project_id`),
  KEY `FDK_documents_uploaded_by_316ea3c5_fk_FDK_users_user_id` (`uploaded_by`),
  KEY `FDK_documents_category_c6dfb646_fk_FDK_categories_category_id` (`category`),
  CONSTRAINT `FDK_documents_category_c6dfb646_fk_FDK_categories_category_id` FOREIGN KEY (`category`) REFERENCES `FDK_categories` (`category_id`),
  CONSTRAINT `FDK_documents_project_id_3a254b12_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`),
  CONSTRAINT `FDK_documents_uploaded_by_316ea3c5_fk_FDK_users_user_id` FOREIGN KEY (`uploaded_by`) REFERENCES `FDK_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_documents` (`document_id`, `document_type`, `title`, `url`, `description`, `file_path`, `uploaded_at`, `project_id`, `uploaded_by`, `category`) VALUES
(1,	'sdf',	'sdf',	'',	'<blockquote>Jsdf\r\n</blockquote><h1>Ahoj</h1>\r\n\r\n<p>Ano:</p>',	'',	'2024-10-27 12:42:31.184989',	18,	NULL,	1),
(5,	'System',	'dd',	'',	's',	'',	'2024-10-27 13:07:32.947970',	2,	NULL,	45),
(6,	'bb',	'aa',	'',	'',	'',	'2024-10-27 13:22:25.555705',	2,	NULL,	45),
(7,	'tes',	'Název',	'',	'',	'',	'2024-10-27 13:25:19.529197',	2,	NULL,	45),
(8,	'vd',	'sd',	'',	'ds',	'',	'2024-10-27 13:29:18.540889',	2,	NULL,	45),
(9,	'sdsd',	'fd',	'',	'sd',	'',	'2024-10-27 13:31:45.679075',	2,	NULL,	45),
(10,	'v',	's',	'',	'',	'',	'2024-10-27 13:39:08.844460',	18,	NULL,	42),
(12,	'adf',	'adf',	'',	'',	'',	'2024-10-28 20:56:57.108000',	36,	NULL,	53),
(13,	'Návrh',	'Prvotní zadání',	'',	'Modulově Příroda - Společnost -	\r\nPřepínač pozadí	\r\nBarvy	\r\nMnemotechnické pomůcky	\r\nOsvěta - Hádanky	\r\nSkupinový aktivity ..	\r\nLabyrinty	\r\n\r\n- oblékací hry\r\n	\r\nGrafomotorika (+ video)	\r\nPosuny obrázku.	\r\nListy stromu - vybrat druh stromu	\r\nZvíře řekne - ukaž lípu	\r\nPoznej zvířata (zoo a podmodul ptáci ap. + hmyz)	\r\nPřehled zvířat a zvuku (info stránka)	\r\nPoznej rostliny	\r\nGalerie zvuků zvířat (rozpoznávání a znělka)	\r\nSpojit produkt a zvíře	\r\nBarvy - (černobílý ovoce a vybavení)	\r\nBarvy semaforu + značky + dopr.prostredky	\r\nGalerie ovoce české a exotické	\r\n(přiřadit do košíků, co najdeme na zahradce, co roste u nás)	\r\nTvary v obrázku a spocitej.\r\n\r\n=== \r\n\r\nA zpětná vazba. (Možnosti obrázků do tvaru )		\r\nUrčí povolání (Telefonní čísla - když nevíš 112)		\r\nZajímavosti modul.		\r\nZvířat a přírody		\r\nSamostatný počítání - 3 jabka		\r\nRoční období - poznej oblečení		\r\nPlanety ? Slunce, země, měsíc (konzultace) Mars Venuse		\r\nPoznej obrázky podle písem A B C D (Obrázková abecede)		\r\nDiverzita etnik		\r\n		\r\n	KATEGORIE	\r\n	Poznávání přírody	\r\n		\r\n		\r\n		\r\n		\r\n		\r\n		\r\nPDF pexeso omalovánky černý Petr		\r\nMarketingu komunitní školy.		\r\nChutě - přiřadit		\r\nLokality (!?)		\r\n	http://usmevnaskola.cz/',	'',	'2024-10-29 18:53:33.203871',	34,	NULL,	64),
(14,	'Návrh',	'Libuše a Přemysl',	'',	'Pověst',	'',	'2024-12-02 13:49:38.370380',	34,	NULL,	48),
(15,	'test',	'test',	'',	'',	'',	'2024-12-02 19:05:28.327604',	34,	NULL,	47),
(16,	'aaa',	'test',	'',	'<p>aasdf asd asdf</p>asdf',	'',	'2024-12-03 21:00:35.676178',	18,	NULL,	42),
(18,	'seznam konkurence',	'Inspirace a zdroje',	'',	'<p>Zdroje, z kterych muzeme brat inspiraci nebo porovnat jestli se nevenuji stejne teme ze stejneho uhlu:<br><br>Petra Nejedla -&nbsp; Vyvoj reci v souvislostech:&nbsp;<a href=\"https://vyvojreci.cz/\" target=\"_blank\">https://vyvojreci.cz/</a></p><p>Vlastnim tempem - Magda Olsinska:&nbsp;<a href=\"https://vlastnimtempem.cz/\" target=\"_blank\">https://vlastnimtempem.cz/</a></p><p>CT Edu:&nbsp;<a href=\"https://edu.ceskatelevize.cz/\" target=\"_blank\">https://edu.ceskatelevize.cz/</a></p><hr><p><a href=\"https://edu.ceskatelevize.cz/\" target=\"_blank\"><br></a></p><p>&nbsp;</p>',	'',	'2024-12-04 20:21:02.565038',	34,	NULL,	64),
(19,	'informace',	'Zapisy ze schuzek',	'',	'<p>13.1.2025</p><p>domluveno</p><p>- Martin pripravi pdf souhlasu k pouziti obrazku od deti</p><p>- Martin doplni bajky&nbsp;</p><p>- Jana sepise hadanky, ktere pripravila</p><p>- Kristina dokonci pracovni listy</p><p>- vygenerovat hadanky pomoci AI</p><p>- Kristina zjisti tipy na AI hlas<br>- Kristina a Jana skusia poptat logo</p><p><br></p><p>6.1.2025<br>domluveno</p><p>- Martin prida baje,</p><p>- Kristina dokonci pracovne listy s pismenami a obrazkami</p><p>- Veronika - pripravi rikanky</p><p>- Jana - pripravi hadanky<br><br>Diskutovane<br>- chybi nam obrazky - na stranku, potencialne do knizky<br>- navrh je nechat vytvorit detma alebo umelou inteligenci<br>- nebo vytvorit vlastni obrazky nebo poptat ilustratora-profesionala</p><p>- poptat seniory ohledne obrazku&nbsp;<br style=\"--tw-border-spacing-x: 0; --tw-border-spacing-y: 0; --tw-translate-x: 0; --tw-translate-y: 0; --tw-rotate: 0; --tw-skew-x: 0; --tw-skew-y: 0; --tw-scale-x: 1; --tw-scale-y: 1; --tw-pan-x: ; --tw-pan-y: ; --tw-pinch-zoom: ; --tw-scroll-snap-strictness: proximity; --tw-gradient-from-position: ; --tw-gradient-via-position: ; --tw-gradient-to-position: ; --tw-ordinal: ; --tw-slashed-zero: ; --tw-numeric-figure: ; --tw-numeric-spacing: ; --tw-numeric-fraction: ; --tw-ring-inset: ; --tw-ring-offset-width: 0px; --tw-ring-offset-color: #fff; --tw-ring-color: rgb(59 130 246 / 0.5); --tw-ring-offset-shadow: 0 0 #0000; --tw-ring-shadow: 0 0 #0000; --tw-shadow: 0 0 #0000; --tw-shadow-colored: 0 0 #0000; --tw-blur: ; --tw-brightness: ; --tw-contrast: ; --tw-grayscale: ; --tw-hue-rotate: ; --tw-invert: ; --tw-saturate: ; --tw-sepia: ; --tw-drop-shadow: ; --tw-backdrop-blur: ; --tw-backdrop-brightness: ; --tw-backdrop-contrast: ; --tw-backdrop-grayscale: ; --tw-backdrop-hue-rotate: ; --tw-backdrop-invert: ; --tw-backdrop-opacity: ; --tw-backdrop-saturate: ; --tw-backdrop-sepia: ; --tw-contain-size: ; --tw-contain-layout: ; --tw-contain-paint: ; --tw-contain-style: ;\"><br>9.12.<br>domluveno<br>- Martin prida baje,<br>- Jana dokonci povesti a nahra spolu s povidaci babickou niektore povesti,<br>- Kristina pripravi pracovne listy,<br>- Jana obejde /nakontaktuje specialny pedagogy ve svem meste,<br>- nejblizsi setkani online: streda 18.12. ve 20.30, pak az po Vanocnich prazninach 6.1. ve 20.30<br><br>4.12.</p><p>domluveno</p><p>- vytvoreni dokumentu s prehledem zdroju/inspiraci/ porovnani pro projekt,</p><p><span style=\"background-color: rgb(255 255 255 / var(--tw-bg-opacity));\">- vytvoreni dokumentu se zapisy schuzek,</span></p><p><span style=\"background-color: rgb(255 255 255 / var(--tw-bg-opacity));\">- rozeslani formularu do svych zajmovych skupin.&nbsp;</span></p><p><br>2.12.<br></p><p>dohodli jsme se na&nbsp;</p><p><br></p><p>- sdílení formuláře pro další směřování projektu.&nbsp;</p><p>- Namluvení bajek a pověstí.&nbsp;&nbsp;</p><p>- Oslovení specialistů v oboru&nbsp;</p><div><br></div><div>27.11.</div><div>domluveno</div><div>- pravidelne video hovory posunuty na 20.30 v pondeli a stredu,</div><div>- spracovani povesti<br><br></div>',	'',	'2024-12-04 20:52:54.515050',	34,	NULL,	64),
(20,	'System',	'Základní příkazy pro práci na serveru',	'',	'<h5 class=\"card-title\" style=\"margin-bottom: var(--bs-card-title-spacer-y); color: rgb(33, 37, 41); font-family: &quot;Helvetica Neue&quot;, Arial, sans-serif;\"><span style=\"font-weight: bolder; color: var(--bs-body-color); font-size: 1rem;\">OBSAH</span><br></h5><ul style=\"font-family: &quot;Helvetica Neue&quot;, Arial, sans-serif;\"><li>Seznámení</li><li>Virtuální prostředí</li><li>Změna oprávnění k souborům</li><li>Řešení problémů s nefunkčním serverem</li></ul><p><b><br></b></p><p><b>Základní příkazy</b> v příkazové řádce linuxového serveru:</p><p><span style=\"font-weight: bolder; font-family: &quot;Helvetica Neue&quot;, Arial, sans-serif; font-size: 18px;\">Seznámení</span><br></p>\r\n<ul>\r\n<li>Po spuštění terminálu se jako první hodí příkaz <code>ls</code>, který nám vypíše obsah adresáře.</li><li>Pro přesouvání se z adresáře do adresáře poslouží příkaz <code>cd název_složky/</code>, např. <code>cd div_app/</code>, kterým se přesuneme z aktuálního adresáře do složky div_app/. Příkaz je možné použít i pro skok o několik úrovní dál, např. <code>cd div_app/div_content/</code></li>\r\n<li>Pro návrat do nadřazeného adresáře využijeme příkaz <code>cd ..</code>&nbsp;</li>\r\n<li>Vytvoření nového souboru provedeme příkazem <code>touch název_souboru.přípona</code>, např. <code> touch index.html</code>. Přejmenování souboru je možné příkazem <code>mv název_souboru nový_název_souboru</code>, např. <code>mv index.html forum_index.html</code></li>.</ul>\r\n<p><b style=\"font-size: 18px; font-family: &quot;Helvetica Neue&quot;, Arial, sans-serif; color: var(--bs-body-color);\">Virtuální prostředí</b><br></p><p>Abychom mohli používat nástroje Djanga, je potřeba si aktivovat virtuální prostředí.</p><ul><li>Před aktivací virtuálního prostředí se ujistíme, že se nacházíme ve složce div_app/, která obsahuje i složku s virtuálním prostředí.&nbsp;</li><li>Samotná aktivace se realizuje příkazem <code>source div_env/bin/activate</code>. O tom, že vše proběhlo v pořádku, se můžeme přesvědčit tím, že v příkazové řádce na daném řádku přibylo&nbsp;<code>(div_env)</code> před naší přezdívkou, např. <code>(div_env) xsilence8x@divcz:/var/www/div_app$</code></li></ul>\r\n<p>Nyní můžeme využívat příkazy jako:</p><p><br></p><ul><li><code>python3 manage.py shell</code></li><li><code>python3 manage.py runserver</code></li><li><code>python3 manage.py makemigrations</code></li><li><code>python3 manage.py migrate</code></li></ul>\r\n<p><br></p><p><font face=\"Helvetica Neue, Arial, sans-serif\"><span style=\"font-size: 18px;\"><b>Změna oprávnění k souborům</b></span></font><br></p><p>Pro editaci souborů na serveru je potřeba získat potřebná oprávnění pro možnost psát kód, zakládat nové soubory, provádět migrace apod. </p><ul><li>Pro výpis uživatelů, kteří mají patřičná oprávnění, použijeme příkaz&nbsp;<code>ls -l</code>. Použití tohoto příkazu ve složce např. div_app/div_content/templates nám vypíše do konzole <code>\r\ntotal 176\r\n-rw-rw-r-- 1 wendy:martin  5237 Aug 18 14:10 403.html\r\n...</code> kde vidíme, že oprávnění mají uživatelé wendy a martin. </li><li>Práva pro editaci celého adresáře templates/ si převedeme na sebe příkazem <code>sudo chown -R xsilence8x:wendy templates/</code> (Můžete si všimnout, že práva jsme zachovali i uživateli wendy).</li></ul>\r\n<p><br></p><p><font face=\"Helvetica Neue, Arial, sans-serif\"><span style=\"font-size: 18px;\"><b>Řešení problémů s nefunkčním serverem</b></span></font><br></p><p>Pokud se při programování něco pokazí, je možné se podívat na aktuální výpis Django aplikace příkazem <code>tail -f nohup.out</code>. Při programování v backendové části se hodí nechat tento log běžet s aktuálním výpisem do konzole (výpis ukončím, resp. z něj vyjedu klávesovou zkratkou Ctrl + C).</p>\r\n<p>Při nejistotě, zdali máme spuštěný server a databázi, je možné se příkazem</p><ul><li> <code>sudo systemctl status nginx</code>&nbsp;pro server a&nbsp;</li><li><code>sudo systemctl status mariadb</code>&nbsp;pro databázi podívat na dané služby.</li></ul>\r\n<p>Pokud je vše v pořádku, příkaz nás informuje zprávou, že vše běží <code> active(running)</code><span style=\"color: var(--bs-body-color); font-size: 1rem;\">. Pokud by tomu bylo jinak, je možné služby uvést do chodu příkazy </span><code>sudo systemctl start nginx</code><span style=\"color: var(--bs-body-color); font-size: 1rem;\"> pro server a </span><code>sudo systemctl start mariadb</code><span style=\"color: var(--bs-body-color); font-size: 1rem;\"> pro databázi.</span><br></p>\r\n<p>Je možné, že posléze bude potřeba spustit i Django server, nejlépe příkazem <code>nohup python3 manage.py runserver &amp;&nbsp;</code></p><p><code><br></code></p><p><code>NEFUNKČNÍ SPUŠTĚNÍ RUNSERVER</code></p><p><font face=\"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace\">Zjištění co běží:&nbsp;</font></p><p><span style=\"font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, &quot;Liberation Mono&quot;, &quot;Courier New&quot;, monospace; font-size: 1em; background-color: rgb(255 255 255 / var(--tw-bg-opacity));\">sudo lsof -i :8000</span><font face=\"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace\"><br></font></p><p></p><p><code><br></code></p><p><code>Ukončení procesu:<br></code></p><p><font face=\"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace\">sudo kill 1234<br>sudo kill - 9 1234</font></p><p><font face=\"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace\"><br></font></p><p><font face=\"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace\">python3 manage.py runserver</font></p><div><br></div><hr><div><br></div><div><br></div>',	'',	'2024-12-04 21:25:21.640453',	37,	NULL,	57),
(21,	'word',	'Říkanky',	'',	'<p><span style=\"background-color: rgb(255, 255, 0);\">Říkanky<br><br></span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">1. Šnečku, šnečku, vystrč růžky</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Šnečku, šnečku, vystrč růžky,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">dám ti krejcar na tvarůžky,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">a troníček na tabáček,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">bude z tebe hajdaláček.</span></p><p><b style=\"font-weight:normal;\" id=\"docs-internal-guid-2cef036f-7fff-5a3f-f002-fd8270186f32\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">2. Pec nám spadla</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Pec nám spadla, pec nám spadla,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">kdo pak nám ji postaví?</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Starý pecař není doma,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">a mladý to neumí.</span></p><p><b style=\"font-weight:normal;\"><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Zavoláme na dědečka,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">ten má velké kladivo,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">zavoláme na babičku,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">ta má zase paličku.</span></p><p><b style=\"font-weight:normal;\"><br></b></p><p><b style=\"font-weight:normal;\"><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">3. Vařila myšička kašičku</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Vařila myšička kašičku</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">na zeleném rendlíčku.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Tomu dala, tomu víc,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">tomu málo, tomu nic.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">A ten maličký,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">utíkal do komůrky,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">tam se napapal.</span></p><p><b style=\"font-weight:normal;\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">4. En ten týky</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">En ten týky, dva špalíky,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">čert vyletěl z elektriky.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Bez klobouku, bos,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">natloukl si nos.</span></p><p><b style=\"font-weight:normal;\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">5. Kutálí se ze dvora</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Kutálí se ze dvora,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">takhle velká brambora.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Neviděla, neslyšela,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">že na ni padá závora.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Kam padáš, ty závoro?</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Na tebe, ty bramboro!</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Kdyby tudy projel vlak,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">byl by z tebe bramborák.</span></p><p><b style=\"font-weight:normal;\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">6. Otloukej se, píšťaličko</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Otloukej se, píšťaličko,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">otloukej se,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">jestli se neotloukáš,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">sama se zlomíš.</span></p><p><b style=\"font-weight:normal;\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">7. Prsty</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Tento prstíček si něco koupil,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">tento prstíček to zaplatil,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">tento prstíček se jen díval,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">tento prstíček jen tak stál</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">a ten maličký…</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">křičel: „Já mám hlad!“</span></p><p><b style=\"font-weight:normal;\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">8. Paci, paci, pacičky</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Paci, paci, pacičky,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">táta koupil botičky,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">a maminka páseček,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">abych chodil do pěšek.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">A když bylo dopoledne,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">začalo to velké běhání,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">maminka nám dala kašičku,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">a teď spinká, andílku.</span></p><p><b style=\"font-weight:normal;\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">9. Žába skáče po blátě</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Žába skáče po blátě,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">koupíme jí na gatě.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Na jaký, na jaký?</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Na zelený strakatý!</span></p><p><b style=\"font-weight:normal;\"><br><br></b></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">10. Had leze z díry</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Had leze z díry,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">vystrkuje kníry,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">za ním leze hadice,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">má červené střevíce.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Bába se ho lekla,</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">na kolena klekla.</span></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">Nic se bábo nelekej,</span></p><p></p><p dir=\"ltr\" style=\"line-height:1.38;margin-top:0pt;margin-bottom:0pt;\"><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\">na kolena neklekej!</span></p><div><span style=\"font-size:11pt;font-family:Arial,sans-serif;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;\"><br></span></div>',	'',	'2025-01-28 11:53:15.411714',	34,	NULL,	63);

CREATE TABLE `FDK_invoice` (
  `invoice_id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(20) NOT NULL,
  `issue_date` date NOT NULL,
  `due_date` date NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `vat_amount` decimal(10,2) NOT NULL,
  `vat_rate` decimal(5,2) NOT NULL,
  `is_paid` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`invoice_id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `FDK_invoice_company_id_59340265_fk_FDK_company_company_id` (`company_id`),
  CONSTRAINT `FDK_invoice_company_id_59340265_fk_FDK_company_company_id` FOREIGN KEY (`company_id`) REFERENCES `FDK_company` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_invoice_item` (
  `invoice_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `vat_rate` decimal(5,2) NOT NULL,
  PRIMARY KEY (`invoice_item_id`),
  KEY `FDK_invoice_item_invoice_id_36dba63c_fk_FDK_invoice_invoice_id` (`invoice_id`),
  CONSTRAINT `FDK_invoice_item_invoice_id_36dba63c_fk_FDK_invoice_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `FDK_invoice` (`invoice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_lists` (
  `list_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `is_private` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`list_id`),
  KEY `FDK_lists_project_id_605e6065_fk_FDK_projects_project_id` (`project_id`),
  KEY `FDK_lists_owner_id_bcf6dd95_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `FDK_lists_owner_id_bcf6dd95_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `FDK_lists_project_id_605e6065_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_lists` (`list_id`, `name`, `description`, `is_private`, `created`, `modified`, `project_id`, `owner_id`) VALUES
(10,	'Inspirace',	'Inspirativní weby.',	0,	'2024-10-29 20:44:52.221011',	'2024-10-31 08:42:42.812379',	NULL,	1),
(11,	'smazat',	'',	0,	'2024-10-30 09:20:20.394317',	'2024-10-30 09:21:13.402951',	NULL,	1),
(13,	'Odkazy',	'Odkazy',	0,	'2024-11-27 19:25:30.992702',	'2024-11-27 19:25:30.997052',	38,	1);

CREATE TABLE `FDK_list_items` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `item_order` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `list_id` int(11) NOT NULL,
  PRIMARY KEY (`item_id`),
  KEY `FDK_list_items_list_id_4a1ec322_fk_FDK_lists_list_id` (`list_id`),
  CONSTRAINT `FDK_list_items_list_id_4a1ec322_fk_FDK_lists_list_id` FOREIGN KEY (`list_id`) REFERENCES `FDK_lists` (`list_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_list_items` (`item_id`, `content`, `item_order`, `created`, `modified`, `list_id`) VALUES
(18,	'https://vlastnimtempem.cz/ - Inspirace pro rodiče dětí s obtížemi ve vývoji',	1,	'2024-10-29 20:47:30.612170',	'2024-10-29 20:47:30.612467',	10),
(19,	'https://proevinku.cz/ - Hry a PDF',	1,	'2024-10-29 20:47:52.686843',	'2024-10-29 20:47:52.687028',	10),
(20,	'https://www.kidedu.cz/ pro děti, rodiče i školy',	1,	'2024-10-29 20:48:20.265713',	'2024-10-29 20:48:20.265891',	10),
(21,	'https://mamadodeste.cz/ - PDF',	1,	'2024-10-30 19:01:19.158466',	'2024-10-30 19:01:19.158736',	10),
(22,	'https://www.digitalniknihovna.cz/nkp/',	1,	'2024-11-27 19:27:14.584300',	'2024-11-27 19:27:14.584638',	13);

CREATE TABLE `FDK_list_permissions` (
  `list_permission_id` int(11) NOT NULL AUTO_INCREMENT,
  `can_edit` tinyint(1) NOT NULL,
  `can_add` tinyint(1) NOT NULL,
  `flist_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`list_permission_id`),
  KEY `FDK_list_permissions_flist_id_879f4df4_fk_FDK_lists_list_id` (`flist_id`),
  KEY `FDK_list_permissions_user_id_7b21cdd2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `FDK_list_permissions_flist_id_879f4df4_fk_FDK_lists_list_id` FOREIGN KEY (`flist_id`) REFERENCES `FDK_lists` (`list_id`),
  CONSTRAINT `FDK_list_permissions_user_id_7b21cdd2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_milestones` (
  `milestone_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`milestone_id`),
  KEY `FDK_milestones_project_id_7545a3bd_fk_FDK_projects_project_id` (`project_id`),
  CONSTRAINT `FDK_milestones_project_id_7545a3bd_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_milestones` (`milestone_id`, `title`, `description`, `due_date`, `status`, `created_at`, `updated_at`, `project_id`) VALUES
(1,	'ABC',	'dd',	NULL,	'in_progress',	'2024-10-28 21:22:50.341281',	'2024-10-28 21:22:50.341312',	18),
(2,	'tse',	'',	NULL,	'not_started',	'2024-10-28 21:33:18.862484',	'2024-10-28 21:33:18.862509',	18),
(3,	'Dokončení abecedy',	'',	'2025-01-31',	'in_progress',	'2024-10-29 18:38:17.424893',	'2024-10-29 18:38:17.424916',	34),
(4,	'Říkanky',	'Sepsání českých známých i méně známých říkanek.',	'2025-02-28',	'in_progress',	'2025-01-28 11:56:06.268500',	'2025-01-28 11:56:06.268533',	34);

CREATE TABLE `FDK_permissions` (
  `permission_id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_name` varchar(255) NOT NULL,
  PRIMARY KEY (`permission_id`),
  UNIQUE KEY `permission_name` (`permission_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_permissions` (`permission_id`, `permission_name`) VALUES
(3,	'delete'),
(9,	'delete_project'),
(6,	'delete_task'),
(12,	'delete_users'),
(2,	'edit'),
(8,	'edit_project'),
(5,	'edit_task'),
(11,	'edit_users'),
(1,	'view'),
(7,	'view_project'),
(4,	'view_task'),
(10,	'view_users');

CREATE TABLE `FDK_projects` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `public` tinyint(1) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created` datetime(6) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  KEY `FDK_projects_owner_id_04d3faff_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `FDK_projects_owner_id_04d3faff_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_projects` (`project_id`, `name`, `description`, `url`, `public`, `start_date`, `end_date`, `created`, `owner_id`) VALUES
(1,	'ahoj projekte',	'',	'',	0,	NULL,	NULL,	NULL,	5),
(2,	'LLL',	'',	NULL,	0,	NULL,	NULL,	NULL,	1),
(3,	'asdfasd fasasdf',	'da',	NULL,	0,	NULL,	NULL,	NULL,	5),
(4,	'daf',	'',	NULL,	0,	NULL,	NULL,	NULL,	5),
(5,	'AB',	'',	'ASDF',	0,	NULL,	NULL,	NULL,	5),
(6,	'Martin2 - avsdc',	'',	'a',	0,	NULL,	NULL,	NULL,	2),
(7,	'jmeno projektu',	'popis projekůtůů',	'url-projek',	0,	NULL,	NULL,	NULL,	2),
(8,	'Martin - projekt nový',	'popis',	'url-projekut',	0,	'2024-09-26',	NULL,	NULL,	6),
(9,	'Martin - projekt nový',	'popis',	'url-projekut',	0,	NULL,	NULL,	NULL,	6),
(10,	'test',	'',	NULL,	0,	NULL,	NULL,	NULL,	6),
(11,	'test44',	'',	NULL,	0,	NULL,	NULL,	NULL,	6),
(12,	'asdf',	'',	NULL,	0,	'2024-09-21',	NULL,	NULL,	6),
(13,	'asdf',	'',	NULL,	0,	'2024-09-21',	NULL,	NULL,	6),
(14,	'asdf',	'',	NULL,	0,	'2024-09-21',	NULL,	NULL,	6),
(15,	'asdf',	'',	NULL,	0,	'2024-09-21',	NULL,	NULL,	6),
(16,	'F DEL',	'',	NULL,	0,	NULL,	NULL,	NULL,	2),
(17,	'A',	'',	NULL,	0,	'2024-09-14',	'2024-09-04',	NULL,	2),
(18,	'Správce FDK.cz',	'Všemocný projektový nástroj.',	'https://fdk.cz',	0,	NULL,	NULL,	NULL,	1),
(19,	'Martinmartin',	'martin',	'maritn',	0,	NULL,	NULL,	NULL,	6),
(20,	'Nový projekt',	'nejnovější projekt',	NULL,	0,	NULL,	NULL,	NULL,	6),
(21,	'Martin',	'',	NULL,	0,	NULL,	NULL,	NULL,	8),
(22,	'ajdůlsakjfů aklsjd fůklajs',	'',	NULL,	0,	NULL,	NULL,	NULL,	6),
(23,	'aůlsdjf lkjlůjk',	'',	NULL,	0,	NULL,	NULL,	NULL,	6),
(24,	'Martin',	's',	'https://div.cz',	0,	NULL,	'2024-10-19',	NULL,	10),
(25,	'nazev',	'aůlsdkj',	NULL,	0,	NULL,	NULL,	NULL,	10),
(26,	'test',	'asd s',	NULL,	0,	'2024-10-27',	NULL,	NULL,	10),
(27,	'test',	'dsaf',	NULL,	0,	NULL,	NULL,	NULL,	10),
(28,	'testě',	'',	NULL,	0,	NULL,	NULL,	NULL,	10),
(29,	's',	'',	NULL,	0,	NULL,	NULL,	NULL,	10),
(30,	'sd',	'',	NULL,	0,	NULL,	NULL,	NULL,	10),
(31,	'Nový projekt IIs',	'',	NULL,	0,	NULL,	NULL,	NULL,	10),
(32,	'Jan Žižka',	'Digitální muzeum Jan Žižka.',	NULL,	0,	'2024-01-01',	NULL,	NULL,	2),
(33,	'Div žes',	'',	NULL,	0,	NULL,	NULL,	NULL,	2),
(34,	'Úsměvná škola',	'Projekt pro předškolní děti.',	'https://usmevnaskola.cz',	0,	NULL,	NULL,	NULL,	1),
(35,	'test2',	'',	NULL,	0,	NULL,	NULL,	NULL,	10),
(36,	'Cesta k dohodě',	'',	'https://cestakdohode.cz',	0,	'2024-10-01',	NULL,	NULL,	1),
(37,	'Databáze DIV.cz',	'',	'https://div.cz',	0,	NULL,	NULL,	NULL,	1),
(38,	'Digitální muzeum',	'',	'https://digitalnimuzeum.cz',	0,	'2024-01-01',	NULL,	NULL,	1),
(39,	'SR',	'test',	NULL,	0,	'2024-11-17',	'2024-11-30',	NULL,	18),
(40,	'a',	'',	NULL,	0,	NULL,	NULL,	NULL,	19),
(41,	'maklerský projekt',	'',	NULL,	0,	NULL,	NULL,	NULL,	29);

DELIMITER ;;

CREATE TRIGGER `trg_after_project_insert` AFTER INSERT ON `FDK_projects` FOR EACH ROW
BEGIN
    INSERT INTO FDK_test_types (name, description, project_id)
    VALUES ('UAT testování', 'Uživatelské akceptační testování', NEW.project_id);
END;;

DELIMITER ;

CREATE TABLE `FDK_project_user` (
  `project_user_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`project_user_id`),
  KEY `FDK_project_user_project_id_ef31d355_fk_FDK_projects_project_id` (`project_id`),
  KEY `FDK_project_user_user_id_8ee8a74f_fk_auth_user_id` (`user_id`),
  KEY `FDK_project_user_role_id_8057b1a7_fk_FDK_roles_role_id` (`role_id`),
  CONSTRAINT `FDK_project_user_project_id_ef31d355_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`),
  CONSTRAINT `FDK_project_user_role_id_8057b1a7_fk_FDK_roles_role_id` FOREIGN KEY (`role_id`) REFERENCES `FDK_roles` (`role_id`),
  CONSTRAINT `FDK_project_user_user_id_8ee8a74f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_project_user` (`project_user_id`, `project_id`, `user_id`, `role_id`) VALUES
(9,	16,	2,	2),
(10,	17,	2,	2),
(11,	18,	1,	2),
(14,	21,	8,	2),
(24,	31,	10,	2),
(26,	33,	2,	2),
(27,	34,	1,	2),
(29,	18,	11,	2),
(31,	34,	10,	4),
(34,	31,	10,	2),
(35,	35,	10,	2),
(36,	36,	1,	2),
(38,	37,	11,	3),
(39,	18,	7,	2),
(40,	36,	8,	1),
(41,	38,	1,	2),
(42,	38,	11,	2),
(43,	34,	12,	2),
(44,	38,	12,	2),
(45,	37,	13,	2),
(46,	18,	13,	2),
(47,	18,	15,	2),
(48,	37,	15,	3),
(49,	34,	16,	2),
(50,	34,	17,	3),
(53,	40,	19,	2),
(54,	37,	20,	2),
(55,	37,	21,	2),
(56,	18,	24,	2),
(57,	34,	26,	2),
(58,	34,	27,	2),
(59,	18,	19,	2),
(60,	38,	26,	2),
(61,	38,	28,	2),
(62,	34,	28,	2),
(63,	37,	1,	2),
(64,	18,	27,	2),
(65,	41,	29,	2),
(66,	37,	16,	2);

CREATE TABLE `FDK_roles` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_roles` (`role_id`, `role_name`) VALUES
(2,	'Administrator'),
(3,	'Editor'),
(1,	'Owner'),
(4,	'Viewer');

CREATE TABLE `FDK_role_permisssions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `FDK_role_permisssions_role_id_permission_id_771785e5_uniq` (`role_id`,`permission_id`),
  KEY `FDK_role_permisssion_permission_id_d5a006fa_fk_FDK_permi` (`permission_id`),
  CONSTRAINT `FDK_role_permisssion_permission_id_d5a006fa_fk_FDK_permi` FOREIGN KEY (`permission_id`) REFERENCES `FDK_permissions` (`permission_id`),
  CONSTRAINT `FDK_role_permisssions_role_id_3ff8dca1_fk_FDK_roles_role_id` FOREIGN KEY (`role_id`) REFERENCES `FDK_roles` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_tasks` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `priority` varchar(16) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `creator_id` varchar(50) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `created` datetime(6) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `assigned_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  KEY `FDK_tasks_category_id_8f3c6e1a_fk_FDK_categories_category_id` (`category_id`),
  KEY `FDK_tasks_project_id_cc66862c_fk_FDK_projects_project_id` (`project_id`),
  KEY `FDK_tasks_assigned_id_58da0f58_fk_auth_user_id` (`assigned_id`),
  KEY `FDK_tasks_parent_id_71d55977_fk_FDK_tasks_task_id` (`parent_id`),
  KEY `FDK_tasks_organization_id_32c192f0_fk_FDK_company_company_id` (`organization_id`),
  CONSTRAINT `FDK_tasks_assigned_id_58da0f58_fk_auth_user_id` FOREIGN KEY (`assigned_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `FDK_tasks_category_id_8f3c6e1a_fk_FDK_categories_category_id` FOREIGN KEY (`category_id`) REFERENCES `FDK_categories` (`category_id`),
  CONSTRAINT `FDK_tasks_organization_id_32c192f0_fk_FDK_company_company_id` FOREIGN KEY (`organization_id`) REFERENCES `FDK_company` (`company_id`),
  CONSTRAINT `FDK_tasks_parent_id_71d55977_fk_FDK_tasks_task_id` FOREIGN KEY (`parent_id`) REFERENCES `FDK_tasks` (`task_id`),
  CONSTRAINT `FDK_tasks_project_id_cc66862c_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_tasks` (`task_id`, `title`, `description`, `priority`, `status`, `creator_id`, `due_date`, `created`, `category_id`, `project_id`, `assigned_id`, `parent_id`, `organization_id`) VALUES
(1,	'nový úkol',	'',	'',	'',	'4',	NULL,	NULL,	2,	21,	1,	NULL,	NULL),
(2,	',,',	'',	'',	'',	'4',	NULL,	NULL,	1,	21,	7,	NULL,	NULL),
(4,	'test',	'asdf',	'Prim',	'Probíhá',	'4',	NULL,	NULL,	1,	21,	2,	NULL,	NULL),
(5,	'název úkolu',	'',	'',	'Nezahájeno',	'4',	NULL,	NULL,	1,	21,	1,	NULL,	NULL),
(6,	'mm',	'',	'',	'Hotovo',	'6',	'2024-10-28',	NULL,	10,	24,	1,	NULL,	NULL),
(7,	'ůůů',	'',	'',	'',	'6',	NULL,	NULL,	11,	24,	10,	NULL,	NULL),
(12,	'nice to h',	'a',	'Normální',	'Nice to have',	'4',	NULL,	NULL,	11,	24,	10,	NULL,	NULL),
(13,	'Přidat do detailu seznamy',	'Do detailu projektu přidat přidružené seznamy.',	'Normální',	'Hotovo',	'4',	NULL,	NULL,	44,	18,	1,	NULL,	NULL),
(14,	'Přidat graf',	'Statistika',	'Normální',	'Hotovo',	'4',	NULL,	NULL,	44,	18,	1,	NULL,	NULL),
(15,	'Oslovit speciální pedagogy',	'Oslovit ke konzultaci a spolupráci',	'Střední',	'Nezahájeno',	'4',	NULL,	NULL,	48,	34,	26,	NULL,	NULL),
(16,	'ss',	'',	'Normální',	'Nezahájeno',	'6',	NULL,	NULL,	31,	31,	10,	NULL,	NULL),
(22,	'asd',	'',	'Normální',	'Nezahájeno',	'6',	NULL,	NULL,	51,	35,	10,	NULL,	NULL),
(23,	'Menu',	'Přidat do menu vytvořit:\r\n1. Nový úkol\r\n2. Nový projekt',	'Normální',	'Nezahájeno',	'3',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(24,	'Statistiky',	'Přidat statistiku úkolů do Dashboardu',	'Normální',	'Hotovo',	'3',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(25,	'Skupiny uživatelů a zobrazení úkolů',	'1. Pro uživatele v rámci firmy možnost přiřadit úkol komukoliv z organizace/ firmy. Možnost si vytvořit organizaci typu “Domov” a taskovat se mezi uživatele  teto skupiny?\r\n\r\n2. Pro samostatného uživatele mimo organizaci možnost přiřadit úkol pouze sobě pokud nevytvoří svoji org viz bod 1',	'Nice to have',	'Nezahájeno',	'3',	NULL,	NULL,	44,	18,	1,	NULL,	NULL),
(26,	'Přehled modulů',	'K diskuzi zda přesunout zobrazení modulu pod dashboardy, nebo pod menu. Za mě pod menu :-)',	'Nízká',	'Nezahájeno',	'3',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(27,	'Přehled dashboardů na hlavní stránce',	'Odkaz pod číslem -  tj. po kliknutí na číslo se zobrazí seznam projektů/ úkolů atp',	'Nízká',	'Nezahájeno',	'3',	NULL,	NULL,	44,	18,	1,	NULL,	NULL),
(28,	'Možnost přidat/ vložit screen do úkolu',	'Možnost vložit screen/ foto  do tohoto pole',	'Nice to have',	'Nezahájeno',	'3',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(29,	'Přehled úkolů',	'Přidat do přehledu:\r\n1. Kdo vytvořil úkol \r\n2. Datum vytvoření úkolu\r\n3. Možnost filtrovat',	'Nízká',	'Nezahájeno',	'3',	NULL,	NULL,	43,	18,	7,	NULL,	NULL),
(30,	'Aktualizace priorit v úkolech',	'1. Nízká\r\n2. Střední\r\n3. Vysoká',	'Nízká',	'Hotovo',	'3',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(31,	'Aktualizace Stavu pro úkoly',	'1. Nezahájeno\r\n2. Zahájeno (Probíhá?)\r\n3. Odloženo',	'Nízká',	'Hotovo',	'3',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(32,	'test nice to have',	'',	'Nice to have',	'Probíhá',	'10',	NULL,	NULL,	42,	18,	1,	NULL,	NULL),
(33,	'Kalendář - nastavit projektové schůzky',	'...',	'Nice to have',	'Nezahájeno',	'10',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(34,	'Abeceda - grafomotorika',	'Vytvořit PDF abecedy, \r\n\r\n- psací verze i tiskací\r\n- lehká, střední a složitá',	'Normální',	'Probíhá',	'10',	NULL,	NULL,	47,	34,	12,	NULL,	NULL),
(35,	'Vytvořit dotazník (poslat Weru a Petovi >> AP)',	'Zpětná vazba od učitelů\r\n\r\n- předat weru pro asistenta pedagoga (AP)\r\n\r\nGoogle forms\r\n\r\nÚvod: \r\n(Info o proč?)\r\n\r\nOtázky:\r\nS čím potřebují předškolní děti nejvíce pomoci.\r\n\r\nKteré hry nejvíce děti baví (název a druh)\r\n(pohybové, deskové, digitální, karetní)',	'Nízká',	'Probíhá',	'10',	NULL,	NULL,	48,	34,	1,	NULL,	NULL),
(36,	'Fotografie dětí',	'Jak používají hry',	'Nízká',	'Nezahájeno',	'10',	NULL,	NULL,	63,	34,	1,	NULL,	NULL),
(37,	'Pilíř: posílit nejslabší stránku dětí',	'',	'Nízká',	'Nezahájeno',	'10',	NULL,	NULL,	48,	34,	1,	NULL,	NULL),
(38,	'Seznam školek k oslovení',	'',	'Nízká',	'Nezahájeno',	'10',	NULL,	NULL,	64,	34,	1,	NULL,	NULL),
(39,	'Vytvořit propagační materiály',	'',	'Střední',	'Nezahájeno',	'10',	NULL,	NULL,	62,	34,	1,	NULL,	NULL),
(40,	'Interaktivní výukový materiály',	'- Galerie zvuků zvířat (rozpoznávání a znělka)',	'Normální',	'Nezahájeno',	'10',	NULL,	NULL,	63,	34,	1,	NULL,	NULL),
(41,	'Kalendář pravidelných meetingů',	'- plánování schůzek\r\n\r\nclass MeetingSchedule(models.Model):\r\n    project = models.ForeignKey(project, on_delete=models.CASCADE)\r\n    creator = models.ForeignKey(User, on_delete=models.CASCADE)\r\n    date = models.DateField()  # Počáteční datum schůzek\r\n    frequency = models.CharField(max_length=50, choices=[\r\n        (\'weekly\', \'Týdně\'),\r\n        (\'biweekly\', \'Každé dva týdny\'),\r\n        (\'monthly\', \'Měsíčně\')\r\n    ])\r\n\r\n    def __str__(self):\r\n        return f\"Schůzky pro projekt {self.project.name} každých {self.frequency} od {self.date}\"\r\n\r\n\r\n\r\nviews.py\r\n\r\nfrom .models import MeetingSchedule\r\nfrom datetime import date\r\n\r\ndef meeting_calendar(request, project_id):\r\n    # Načítání schůzek projektu\r\n    meetings = MeetingSchedule.objects.filter(project_id=project_id)\r\n    return render(request, \'project/meeting_calendar.html\', {\'meetings\': meetings})\r\n\r\n\r\nHTML\r\n<div class=\"container mx-auto mt-5 px-4 max-w-screen-lg\">\r\n    <h2 class=\"text-lg font-semibold text-gray-700 mb-4\">{% trans \"Termín pravidelných schůzek\" %}</h2>\r\n\r\n    <!-- Kalendář -->\r\n    <div id=\"calendar\"></div>\r\n</div>\r\n\r\n<!-- FullCalendar knihovna -->\r\n<link href=\"https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css\" rel=\"stylesheet\">\r\n<script src=\"https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js\"></script>\r\n<script src=\"https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/locales-all.min.js\"></script>\r\n\r\n<script>\r\n    document.addEventListener(\'DOMContentLoaded\', function () {\r\n        const calendarEl = document.getElementById(\'calendar\');\r\n        const calendar = new FullCalendar.Calendar(calendarEl, {\r\n            initialView: \'dayGridMonth\',\r\n            locale: \'cs\',  // Nastavení kalendáře do češtiny\r\n            events: [\r\n                {% for meeting in meetings %}\r\n                {\r\n                    title: \"Pravidelná schůzka\",\r\n                    start: \"{{ meeting.date }}\",\r\n                    recurrence: \"{{ meeting.frequency }}\",  // Řídí frekvenci\r\n                },\r\n                {% endfor %}\r\n            ],\r\n            eventSources: [\r\n                {\r\n                    url: \'/api/holidays/\',  // API pro české svátky\r\n                    color: \'#FF0000\',       // Červená barva pro svátky\r\n                    textColor: \'white\',\r\n                },\r\n            ]\r\n        });\r\n        calendar.render();\r\n    });\r\n</script>\r\n\r\n\r\nSVÁTKY\r\nfrom django.http import JsonResponse\r\nfrom datetime import date\r\n\r\ndef holiday_api(request):\r\n    # Statický seznam českých státních svátků\r\n    holidays = [\r\n        {\"date\": \"2024-01-01\", \"title\": \"Nový rok\"},\r\n        {\"date\": \"2024-05-01\", \"title\": \"Svátek práce\"},\r\n        # Další svátky\r\n    ]\r\n    return JsonResponse(holidays, safe=False)',	'Nice to have',	'Nezahájeno',	'10',	NULL,	NULL,	44,	18,	1,	NULL,	NULL),
(42,	'e-shop',	'https://div.cz/eshop/',	'Nízká',	'Probíhá',	'10',	NULL,	NULL,	57,	37,	1,	NULL,	NULL),
(43,	'Karetní hry',	'- zvířátka + produkty\r\n\r\npes + kost\r\nslon + list\r\nlev + maso',	'Nízká',	'Nezahájeno',	'10',	NULL,	NULL,	49,	34,	1,	NULL,	NULL),
(44,	'Logopedické pomůcky',	'',	'Nízká',	'Nezahájeno',	'10',	NULL,	NULL,	63,	34,	1,	NULL,	NULL),
(45,	'React',	'',	'Nice to have',	'Nezahájeno',	'10',	NULL,	NULL,	43,	18,	1,	NULL,	NULL),
(46,	'test uložení data vytvoření',	'5',	'Nízká',	'Nezahájeno',	'10',	NULL,	'2024-10-31 06:02:11.804008',	42,	18,	1,	NULL,	NULL),
(47,	'řazení herců u film',	'nastavit řazení dle \"popularity\"? \r\nNakešovat',	'Nízká',	'Nezahájeno',	'10',	NULL,	'2024-11-10 10:00:27.347812',	57,	37,	1,	NULL,	NULL),
(48,	'GDPR interní audit',	'',	'Nízká',	'Probíhá',	'10',	NULL,	'2024-11-15 18:29:41.893919',	44,	18,	1,	NULL,	NULL),
(49,	'infostranka se službami pro zákazníka',	'fdk.cz/',	'Nízká',	'Nezahájeno',	'10',	NULL,	'2024-11-15 18:47:09.166429',	44,	18,	1,	NULL,	NULL),
(50,	'1',	'sestava polozek',	'Nízká',	'Hotovo',	'14',	NULL,	'2024-11-16 12:07:55.635034',	67,	39,	18,	NULL,	NULL),
(51,	'3D skenery - rešerže trhu',	'- rozlišení\r\n- kvalita modelu\r\n- rychlost skenu',	'Nízká',	'Nezahájeno',	'10',	NULL,	'2024-11-17 10:45:12.973394',	59,	38,	1,	NULL,	NULL),
(52,	'3D artefakty - import jiných souborů',	'- fbx funkční\r\n- obj - přidat jako variantu\r\n- blender (volitelně)',	'Nízká',	'Probíhá',	'10',	NULL,	'2024-11-17 10:59:12.421243',	59,	38,	1,	NULL,	NULL),
(53,	'Sehnat 3D modely',	'- AI (clau\r\n- skrz skener (navazat spolupráci s muzei a sběrateli)\r\n- skrz online knihovny modelů\r\n- vývoj vlastního modelu\r\n\r\nhttps://www.alpha3d.io/ (od 1USD, 50 modelů zdarma)\r\nhttps://www.meshy.ai/\r\nhttps://www.3daistudio.com/',	'Nízká',	'Probíhá',	'10',	NULL,	'2024-11-17 11:13:54.670649',	59,	38,	1,	NULL,	NULL),
(54,	'3D prostor pro artefakt',	'Vytvořit imitaci muzejního prostoru pro zobrazení artefaktu',	'Nízká',	'Nezahájeno',	'10',	NULL,	'2024-11-17 11:17:37.597758',	59,	38,	1,	NULL,	NULL),
(55,	'Namluvit a vytvořit audio verzi českých bájí a pověstí',	'audio verze: \r\n- Šemík (Verča)\r\n- Praotec Čech (Pavla)\r\n- Dívčí války\r\n\r\npropojit s dalšími vzdělávacími aktivitami\r\n- mezipředmětové vztahy (výtvarka, sluch, jaké písmenko, rýmy...)',	'Vysoká',	'Nezahájeno',	'1',	NULL,	'2024-11-18 21:47:40.598024',	63,	34,	1,	NULL,	NULL),
(56,	'Logopedy - oslovit specialisty',	'',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-11-20 19:57:59.582482',	64,	34,	26,	NULL,	NULL),
(57,	'Struktura - Game tabulka',	'Potřebuju upravit tabulky následovně :\r\n1) Game :\r\nRatingID > RawgIO\r\n++ přidat sloupec MetaCritic ( int )\r\n-- smazat sloupce DeveloperID, GenreID,PlatformID, PublisherID\r\n2) Vytvorit tabulky pro metadata\r\nMetaDeveloper - \r\nDeveloperID -- PK || Developer -- varchar || DeveloperURL --varchar unique || RawgID -- int \r\n\r\nMetaPublisher -\r\nPublisherID -- PK || Publisher --varchar || PublisherURL -- varchar || RawgID -- int\r\n\r\n3) Vytvorit propojovaci tabulky\r\nGameDevelopers -\r\nGameDeveloperID -- PK || GameID -- FK Game || DeveloperID -- FK MetaDeveloper\r\n\r\nGamePublisher -\r\nGamePublisherID -- PK || GameID -- FK Game || Publisher -- FK MetaPublisher\r\n\r\n4) Upravit tabulku \r\nGamePlatform -\r\npridat GamePlatformID -- PK , PlatformID = FK na MetaPlatform, GameID = FK na Game',	'Vysoká',	'Hotovo',	'13',	NULL,	'2024-11-24 21:42:48.552305',	58,	37,	1,	NULL,	NULL),
(58,	'SWOT ANALÝZA',	'',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-11-25 19:32:40.060501',	44,	18,	1,	NULL,	NULL),
(59,	'GANTŮV GRAF',	'',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-11-25 19:32:54.575596',	44,	18,	1,	NULL,	NULL),
(60,	'Slovní zásoba (aktivní + pasivní)',	'- čtením\r\n- spojováním písmenek\r\n- dokončit větu vlastními slovy',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-11-25 19:34:23.150631',	63,	34,	1,	NULL,	NULL),
(61,	'Odkaz na narodní knihovnu',	'.-',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-11-27 19:24:59.589348',	61,	38,	1,	NULL,	NULL),
(62,	'vymyslet kategorie pro web',	'- Kronika\r\n- Život a rodina\r\n- Kosmas a jeho doba',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-11-27 19:28:26.668083',	60,	38,	1,	NULL,	NULL),
(67,	'Sehnat medialní zastoupení',	'- oslovit studenty/tky VŠ historie',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-12-08 09:17:50.594968',	59,	38,	1,	NULL,	NULL),
(68,	'Úložiště modelů (cloud)',	'- server 10GB\r\n- cloudový úložiště - \r\n- NAS x',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-12-08 09:23:58.992321',	59,	38,	1,	NULL,	NULL),
(69,	'Opravit scrollování u zpráv',	'Při chatu s jiným uživatelem v sekci zprávy je defaultně nastaveno nascrollovat celou stránku dolů (dle id poslední poslané zprávy). Opravit na stav, kdy je při otevření zprávy nascrollováno dolů jen v rámci chat containeru.',	'Střední',	'Hotovo',	'21',	NULL,	'2024-12-08 15:44:16.662323',	56,	37,	20,	NULL,	NULL),
(70,	'Přenos dat TVShows',	'Přenos dat z testu > produkce\r\n\r\nPořadí :\r\n\r\nCreators>CharactersMeta>MetaGenre>MetaKeyword>MetaProduction>MetaUniversum>TVShow > vse kolem',	'Vysoká',	'Nezahájeno',	'13',	NULL,	'2024-12-08 21:15:58.673105',	58,	37,	1,	NULL,	NULL),
(71,	'Univerzity a školy',	'Studenti historie a dějepisu\r\nRešerže škol - skupina FB\r\n- UJEP (Univerzita Jan Evangelista Purkyně) Ustí n.L',	'Nízká',	'Nezahájeno',	'1',	NULL,	'2024-12-09 19:19:55.803587',	71,	38,	26,	NULL,	NULL),
(72,	'Pracovni listy - Povesti',	'',	'Střední',	'Nezahájeno',	'27',	NULL,	'2024-12-09 19:46:24.553892',	63,	34,	27,	NULL,	NULL),
(73,	'vytoovorit kalendar',	'',	'Nízká',	'Probíhá',	'29',	NULL,	'2024-12-18 14:36:48.004811',	73,	41,	29,	NULL,	NULL),
(74,	'propojit kalendar s  kontaktem',	'',	'Nízká',	'Nezahájeno',	'29',	NULL,	'2024-12-18 14:46:58.951395',	72,	41,	29,	NULL,	NULL),
(75,	'tabulka s nazvem projektu - kontakt  - ukol ?',	'',	'Nízká',	'Nezahájeno',	'29',	NULL,	'2024-12-18 14:47:41.313447',	72,	41,	29,	NULL,	NULL);

CREATE TABLE `FDK_tests` (
  `test_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `grid_location` varchar(2) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `project_id` int(11) NOT NULL,
  `test_type_id` int(11) NOT NULL,
  PRIMARY KEY (`test_id`),
  KEY `FDK_tests_test_type_id_bd548a07_fk_FDK_test_types_test_type_id` (`test_type_id`),
  KEY `FDK_tests_project_id_a7c9d49b_fk_FDK_projects_project_id` (`project_id`),
  CONSTRAINT `FDK_tests_project_id_a7c9d49b_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`),
  CONSTRAINT `FDK_tests_test_type_id_bd548a07_fk_FDK_test_types_test_type_id` FOREIGN KEY (`test_type_id`) REFERENCES `FDK_test_types` (`test_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_tests` (`test_id`, `name`, `description`, `grid_location`, `date_created`, `project_id`, `test_type_id`) VALUES
(1,	'můj test',	'ůalsjd fůalksjd ůfakj dsfůlkaj sdůflkaj sdůfl\r\n\r\nůalkjsd ůflakj sdfů',	'b1',	'2024-09-16 16:32:20.766879',	11,	5),
(2,	'tess',	'asdf',	'a3',	'2024-09-16 16:52:32.363904',	11,	5),
(3,	'aaa',	'',	'b1',	'2024-09-16 17:02:50.819066',	10,	7),
(4,	'uat test',	'alsdjf ůalksd',	'b2',	'2024-09-16 18:58:26.541592',	11,	5),
(5,	'tes',	'',	'a1',	'2024-10-02 15:58:58.905625',	21,	16);

CREATE TABLE `FDK_test_errors` (
  `test_error_id` int(11) NOT NULL AUTO_INCREMENT,
  `error_title` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `steps_to_replicate` longtext DEFAULT NULL,
  `test_result_id` int(11) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `project_id` int(11) NOT NULL,
  `status` varchar(50) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`test_error_id`),
  KEY `FDK_test_errors_project_id_4504c30a_fk_FDK_projects_project_id` (`project_id`),
  KEY `FDK_test_errors_created_by_id_093382f8_fk_auth_user_id` (`created_by_id`),
  KEY `FDK_test_errors_test_result_id_7150bfda_fk_FDK_test_` (`test_result_id`),
  CONSTRAINT `FDK_test_errors_created_by_id_093382f8_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `FDK_test_errors_project_id_4504c30a_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_test_errors` (`test_error_id`, `error_title`, `description`, `steps_to_replicate`, `test_result_id`, `date_created`, `project_id`, `status`, `created_by_id`) VALUES
(1,	'test',	'asd',	'a',	NULL,	'2024-09-16 18:42:03.890241',	11,	'open',	NULL),
(2,	'test3',	'asdf',	'',	NULL,	'2024-09-16 19:03:23.928147',	11,	'open',	NULL),
(3,	'test3',	'asdf',	'',	NULL,	'2024-09-16 19:04:04.703844',	11,	'open',	NULL),
(4,	'test3',	'asdf',	'',	NULL,	'2024-09-16 19:04:08.391733',	11,	'open',	NULL),
(5,	'test3',	'asdf',	'',	NULL,	'2024-09-16 19:04:29.646833',	11,	'open',	NULL),
(6,	'ahoj',	'haoj',	'',	NULL,	'2024-09-16 19:04:45.191912',	11,	'open',	NULL),
(7,	'chyba chyb',	'',	'',	NULL,	'2024-09-16 19:06:37.634250',	11,	'open',	NULL),
(8,	'testasdf',	'',	'',	NULL,	'2024-09-16 19:43:39.755097',	11,	'open',	NULL),
(9,	'testasdf',	'',	'',	NULL,	'2024-09-16 19:49:03.655289',	11,	'open',	NULL),
(10,	'tes',	'',	'',	NULL,	'2024-10-02 15:59:15.780496',	21,	'open',	NULL),
(16,	'test',	'',	'',	NULL,	'2024-10-28 19:30:12.270132',	34,	'open',	NULL),
(19,	'test',	'',	'',	NULL,	'2024-10-28 19:31:06.114016',	37,	'open',	NULL),
(26,	'Ahoj',	'jsem chyba',	'alsdf ůlk aůsd',	NULL,	'2024-10-28 20:52:49.795340',	18,	'open',	NULL),
(30,	'Ahoj',	'jxx',	'',	NULL,	'2024-11-03 08:15:29.865829',	18,	'open',	11);

CREATE TABLE `FDK_test_results` (
  `test_result_id` int(11) NOT NULL AUTO_INCREMENT,
  `result` varchar(50) NOT NULL,
  `execution_date` datetime(6) NOT NULL,
  `executed_by` int(11) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `test_id` int(11) NOT NULL,
  PRIMARY KEY (`test_result_id`),
  KEY `FDK_test_results_executed_by_363030e5_fk_FDK_users_user_id` (`executed_by`),
  KEY `FDK_test_results_project_id_6be07c87_fk_FDK_projects_project_id` (`project_id`),
  KEY `FDK_test_results_test_id_3130a070_fk_FDK_tests_test_id` (`test_id`),
  CONSTRAINT `FDK_test_results_executed_by_363030e5_fk_FDK_users_user_id` FOREIGN KEY (`executed_by`) REFERENCES `FDK_users` (`user_id`),
  CONSTRAINT `FDK_test_results_project_id_6be07c87_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`),
  CONSTRAINT `FDK_test_results_test_id_3130a070_fk_FDK_tests_test_id` FOREIGN KEY (`test_id`) REFERENCES `FDK_tests` (`test_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_test_types` (
  `test_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`test_type_id`),
  KEY `FDK_test_types_project_id_3341ceaa_fk_FDK_projects_project_id` (`project_id`),
  CONSTRAINT `FDK_test_types_project_id_3341ceaa_fk_FDK_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_test_types` (`test_type_id`, `name`, `description`, `project_id`) VALUES
(3,	'algoritm',	'',	12),
(4,	'typ44',	'te',	11),
(5,	'UAT testování',	'',	11),
(6,	'Integrační testování',	'',	13),
(7,	'asdfa',	'',	10),
(8,	'asd',	'',	11),
(9,	'typ44tes',	'',	11),
(10,	'test',	'',	11),
(11,	'a',	'asdf',	9),
(12,	'a',	'',	9),
(13,	'a',	'',	9),
(14,	'a',	'',	9),
(15,	'sd',	'',	10),
(16,	'type',	'alsdjf',	21),
(17,	'UAT testování',	'Uživatelsky akceptační testování',	34),
(18,	'typ testůd',	'lkjl',	31),
(19,	'UAY',	'a',	31),
(20,	'asd',	'',	31),
(21,	'UAT testování',	'Uživatelské akceptační testování',	35),
(22,	'UAT testování',	'Uživatelské akceptační testování',	36),
(23,	'UAT testování',	'Uživatelské akceptační testování',	37),
(24,	'UAT testování',	'Uživatelské akceptační testování',	38),
(25,	'nový typ testu',	'test',	18),
(26,	'UAT testování',	'Uživatelské akceptační testování',	39),
(27,	'UAT testování',	'Uživatelské akceptační testování',	40),
(28,	'UAT testování',	'Uživatelské akceptační testování',	41);

CREATE TABLE `FDK_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  `created` datetime(6) DEFAULT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `FDK_users` (`user_id`, `username`, `password_hash`, `email`, `description`, `created`, `last_login`) VALUES
(3,	'Lenka',	'pbkdf2_sha256$870000$Y14ZU0uZfmxTIGv9K8MyeR$MN1cj1y2in7ehkvs/t77NcDQXnZ6xRtrDZdA6/CNbJE=',	'Lenka_Frankova@outlook.com',	NULL,	'2024-09-24 19:03:12.949532',	NULL),
(4,	'martin.kucera',	'pbkdf2_sha256$870000$FPCCmhjqrpvBBUxYWLBiHm$BEJs8swnyueNydUxAYKyGY1w/IHMYWzuIHmXAAQDIL8=',	'veronika@kucerova2.eu',	NULL,	'2024-10-02 14:59:19.358277',	NULL),
(5,	'Fafol',	'pbkdf2_sha256$870000$sKt6msk7wAf2n7C1M2176P$3zGBlqIXd34Y9+1XDrQIXUHpkN7vgMthHy7piSq2+lI=',	'fafol@fafol.cz',	NULL,	'2024-10-26 07:13:44.324611',	NULL),
(6,	'testik',	'pbkdf2_sha256$870000$qNRA3zATqMe4L63NkkYjjD$b0j4Bq+W+iXJ/w/x85PIEO2WtYKL3Y4kX1pUOYseTGs=',	'test22@test.cc',	NULL,	'2024-10-26 07:54:44.496202',	NULL),
(7,	'Baruuuuuu',	'pbkdf2_sha256$870000$VCzHhcWETO9nU0x23ojDKH$r8/x2VadyMOn0vEm3L2lhA6wTM/fY5uBprp5wXJ4DYQ=',	'ohnivacek123@gmail.com',	NULL,	'2024-10-27 20:07:16.500581',	NULL),
(8,	'werru',	'pbkdf2_sha256$870000$PHobJN4xe7cd7ix9g7tgFZ$4cKsHSxRExn0N664WfHOxhP03lAuo4G32GGuQ8PU3ZE=',	'lamune02@gmail.com',	NULL,	'2024-10-29 18:13:31.148403',	NULL),
(9,	'ionno',	'pbkdf2_sha256$870000$PgGYPdGF65Q4FhnaY6zV3r$A2ICvwuE6Kr+IG90SaRl+GzaSW6n7PKR1+dkpwD4kIQ=',	'illnezz@centrum.cz',	NULL,	'2024-10-29 20:57:12.007400',	NULL),
(10,	'martin10',	'pbkdf2_sha256$870000$iYm2yzfH8wzeZgdOBMpQFj$9p8JF4hahlpKYDVQfgdXTgRIxsvdZqyc6KGjZPdjBew=',	'martin@esmobil.cz',	NULL,	'2024-10-29 21:05:19.759023',	NULL),
(11,	'Misa',	'pbkdf2_sha256$870000$taokRGdeU7aTa3wLN3kBju$h/U1R/iN6LVRzt6hdwFdHDcouRq8Np08LQJS7vvKpF0=',	'aellea.lipenska@gmail.com',	NULL,	'2024-10-30 17:54:31.853748',	NULL),
(12,	'Bershee',	'pbkdf2_sha256$870000$p1yaqGqbkw8B6WsCUWKZ3e$Y8pxFnVxgkInzPKj9NRBipc2GhlZXqQPqC3NwPH8fXw=',	'berankovap90@gmail.com',	NULL,	'2024-10-30 18:12:10.379660',	NULL),
(13,	'PetrHrdina',	'pbkdf2_sha256$870000$kPVfIlk8tL1gzmfwc8iYN4$ldK9rKTyKS/u4PUhA+e2pSy0U2K8fCW51Uu3y5Vw3gw=',	'shorty.one@seznam.cz',	NULL,	'2024-10-30 18:32:40.553791',	NULL),
(14,	'SimonR',	'pbkdf2_sha256$870000$RiHnFxdwQrD0DSzhYV9pQZ$RHN5a+Hc7lsm3slUOpynWlImp1wTHixpi5GaW/WOZQ0=',	'masmer01@yahoo.com',	NULL,	'2024-11-16 12:05:29.975786',	NULL),
(15,	'juraj',	'pbkdf2_sha256$870000$k9GbSwB1YwwPZxfCqqcfHb$kBp8QfMqb3bSmln2cf2ZB6HNoq1CYoYCI05Th27AQKY=',	'a@a.com',	NULL,	'2024-11-17 18:00:49.709915',	NULL),
(16,	'VendaCiki',	'pbkdf2_sha256$870000$vpWkTLZxiplNfM8q4I3zM2$Au9YIOTLUBwPMiZ7kABZiAX0ULG3tG+LVjyODQ+22w4=',	'vendaciki@seznam.cz',	NULL,	'2024-11-18 18:02:10.472443',	NULL),
(17,	'xsilence8x',	'pbkdf2_sha256$870000$RKipLUwBPFURWMuugCNb3u$c3e2siIQaKzi0GNenR1FyNiUqzOLQWIrGLK5KFuJHNs=',	'xsilence8x@hotmail.com',	NULL,	'2024-11-22 08:25:21.954966',	NULL),
(20,	'jirka',	'pbkdf2_sha256$870000$DzpwmO3anzCPB9MjPJil8b$HHFvEh6SvnPhkt28LrNAL6WeJeOnhbBQj7ajwi2H1Ps=',	'jirkha13@gmail.com',	NULL,	'2024-11-24 11:50:37.415046',	NULL),
(21,	'Testtest',	'pbkdf2_sha256$870000$nyRmHHBuHTUiXBXYMvCSUO$gcGUkp7zyAvadGQEiYSoEAMi+Nuf3F2jSJdkpwq2EUk=',	'martin@martin.ma',	NULL,	'2024-11-26 05:51:02.437239',	NULL),
(22,	'JanaS',	'pbkdf2_sha256$870000$g9Cs44kjaNN5Ktcwuoh9ho$er9fmEeFeNXjVY0ax4E95zXzAhe/2dt72WvPCPvvazg=',	'Jana.sot@seznam.cz',	NULL,	'2024-11-26 06:38:36.933707',	NULL),
(23,	'lascalca',	'pbkdf2_sha256$870000$tjg2tNbvu86hejCOPK4lOa$uSNYRFQjTVarpDNwBDAUoN4TIVZkDfI1bKZeuTFvFbE=',	'kkasalova.professional@gmail.com',	NULL,	'2024-11-26 08:38:37.149890',	NULL),
(24,	'SonaJirotova',	'pbkdf2_sha256$870000$r8VXoXAHu5JttQPwAGG2ad$OG2hOmvOnanYa3FQ3Vk0yYws1ENgI/NII3QC0aj0Rho=',	'sjirotova@seznam.cz',	NULL,	'2024-11-27 16:59:55.878562',	NULL),
(25,	'Martin22',	'pbkdf2_sha256$870000$5YsHcWAO1Ea3GID5447ijp$jxiOgJ0E4Qwov6nvWTWjk5iS4rQ9HhCLgD81FhSNZy8=',	'martin1.kucera@t-mobile.cz',	NULL,	'2024-12-18 14:35:24.824049',	NULL),
(26,	'Donaldalimi',	'pbkdf2_sha256$870000$Lzhht6gBcW6IVDRiipTspq$hPoewrGTfEsgqOy/tSCstO3uEps5NenpIELOScdXiLI=',	'donetsk-minsk@bin-bamg.store',	NULL,	'2025-01-11 16:46:51.153409',	NULL),
(27,	'Shawnsum',	'pbkdf2_sha256$870000$gi7vxerwNZTsruzDHxKqa1$yZ4N0BdURPn2mKdoRmp51JJ4eCYLrTfKMbCxW41AmPY=',	'poezdki-v-rostov@bin-bamg.store',	NULL,	'2025-01-11 16:47:52.108665',	NULL),
(28,	'WoodrowFaimb',	'pbkdf2_sha256$870000$vMoad08TRVMJwk9d9jYCmu$SEJyorQIo8MBjWVSuyL7vX1bepN40occbBXTFsc0ubM=',	'festore@bin-bamg.store',	NULL,	'2025-01-11 20:09:04.231449',	NULL),
(29,	'Dennistuh',	'pbkdf2_sha256$870000$Gow9rQm17PDfOtRk0I5LZL$eV7r1xifgOGZWKElSj678QUYgoPEj8QTS1wCwrpfd3E=',	'uslugi_advokata@bin-bamg.ru',	NULL,	'2025-01-22 00:47:28.056294',	NULL),
(30,	'RonaldNiz',	'pbkdf2_sha256$870000$ufVtDJdM4mcqiDVIAVimQ9$TB7YOoKOkvXmr3nNYi/SG3TkKHGiTEaAclKTZIAm3y4=',	'festore@bin-bamg.ru',	NULL,	'2025-02-06 16:46:54.851093',	NULL),
(31,	'Walternix',	'pbkdf2_sha256$870000$T4H4C1Zdpu3jJowuLUU3Dc$vK98HaHwIT4OaQaofAmUcbOnSiESYVp855nr0IgZmNs=',	'donetsk-minsk@bin-bamg.ru',	NULL,	'2025-02-06 16:47:29.847474',	NULL);

CREATE TABLE `FDK_warehouse` (
  `warehouse_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`warehouse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_warehouse_item` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `created` datetime(6) NOT NULL,
  `warehouse_id` int(11) NOT NULL,
  PRIMARY KEY (`item_id`),
  KEY `fdk_cz_item_warehouse_id_dfebea47_fk_fdk_cz_wa` (`warehouse_id`),
  CONSTRAINT `fdk_cz_item_warehouse_id_dfebea47_fk_fdk_cz_wa` FOREIGN KEY (`warehouse_id`) REFERENCES `FDK_warehouse` (`warehouse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_warehouse_transaction` (
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_type` varchar(10) NOT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `date` datetime(6) NOT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `fdk_cz_transaction_item_id_d07eaa22_fk_fdk_cz_item_item_id` (`item_id`),
  CONSTRAINT `fdk_cz_transaction_item_id_d07eaa22_fk_fdk_cz_item_item_id` FOREIGN KEY (`item_id`) REFERENCES `FDK_warehouse_item` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_warehouse_users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `warehouse_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `FDK_warehouse_users_warehouse_id_user_id_03b5c421_uniq` (`warehouse_id`,`user_id`),
  KEY `FDK_warehouse_users_user_id_ce56952e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `FDK_warehouse_users_user_id_ce56952e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `FDK_warehouse_users_warehouse_id_662329d5_fk_FDK_wareh` FOREIGN KEY (`warehouse_id`) REFERENCES `FDK_warehouse` (`warehouse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 2025-02-22 12:28:07

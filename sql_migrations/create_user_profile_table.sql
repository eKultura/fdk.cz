-- SQL migrace pro vytvoření tabulky FDK_user_profile
-- Spustit na produkční databázi

CREATE TABLE IF NOT EXISTS `FDK_user_profile` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `is_vip` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'VIP uživatelé mají vyšší limity projektů',
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_id` (`user_id`),
    CONSTRAINT `FDK_user_profile_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Profily uživatelů s VIP statusem';

-- Vytvoříme profily pro všechny existující uživatele
INSERT IGNORE INTO `FDK_user_profile` (`user_id`, `is_vip`, `created_at`, `updated_at`)
SELECT
    id,
    0,
    NOW(),
    NOW()
FROM `auth_user`;

-- Zaznamenat migraci jako provedenou
INSERT INTO `django_migrations` (`app`, `name`, `applied`)
VALUES ('fdk_cz', '0023_add_user_profile', NOW());

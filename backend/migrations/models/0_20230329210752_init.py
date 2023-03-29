from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `auth_users` (
    `user_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '유저 아이디',
    `name` VARCHAR(255)   COMMENT '이름',
    `email` VARCHAR(255)   COMMENT '이메일',
    `password` VARCHAR(255)   COMMENT '비밀번호'
) CHARACTER SET utf8mb4 COMMENT='인증유저 테이블';
CREATE TABLE IF NOT EXISTS `login_log` (
    `login_log_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '로그인 로그 고유번호',
    `created_at` DATETIME(6) NOT NULL  COMMENT '날짜' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL COMMENT '유저 고유번호',
    CONSTRAINT `fk_login_lo_auth_use_b50ae119` FOREIGN KEY (`user_id`) REFERENCES `auth_users` (`user_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='로그인 로그';
CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '유저 아이디',
    `name` VARCHAR(255)   COMMENT '이름',
    `email` VARCHAR(255)   COMMENT '이메일',
    `password` VARCHAR(255)   COMMENT '비밀번호'
) CHARACTER SET utf8mb4 COMMENT='유저 테이블';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

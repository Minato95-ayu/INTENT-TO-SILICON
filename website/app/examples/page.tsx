import React from 'react';
import Link from 'next/link';
import { ArrowRight, Code } from 'lucide-react';

export default function ExamplesPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-5xl">
        <div className="mb-12">
          <h1 className="text-5xl font-bold mb-6 tracking-tight">Enterprise Examples</h1>
          <p className="text-xl text-zinc-400 max-w-3xl">
            See how AAYU scales to build massive, real-world microservices with built-in memory safety and zero dependencies.
          </p>
        </div>

        <div className="bg-zinc-900/50 border border-white/5 rounded-2xl p-8 mb-12">
          <div className="flex items-center mb-6">
            <Code className="text-emerald-400 w-6 h-6 mr-3" />
            <h2 className="text-2xl font-bold">Full-Stack E-Commerce API</h2>
          </div>
          <p className="text-zinc-400 mb-6">
            This example demonstrates AAYU's ability to handle complex relational data models (Structs), database synchronization, JWT authentication, and transactional integrity for a scalable e-commerce backend.
          </p>
          <div className="bg-black border border-white/10 rounded-xl p-6 overflow-x-auto">
            <pre className="text-sm font-mono text-zinc-300">
              <code>{`app EnterpriseShop

# 1. Complex Memory-Safe Data Models (Structs)
model User
    id Int
    email String
    password_hash String
    role String = "CUSTOMER"
end

model Product
    id Int
    name String
    price Float
    stock_count Int
end

model Order
    id Int
    user_id Int
    total_amount Float
end

# 2. Database Sync
action init_db
    User.sync()
    Product.sync()
    Order.sync()
end

# 3. Enterprise REST API Routes
route "/api/v1/auth/login"
    post
        let user = User.find(email == req.body.email)
        if user.password_hash == req.body.password
            respond({"token": "JWT_AAYU_SECURE_TOKEN_9384"})
        else
            respond({"error": "Invalid"}, 401)
        end
    end
end

route "/api/v1/orders/checkout"
    post
        let target_product = Product.findById(req.body.product_id)
        if target_product.stock_count > 0
            target_product.stock_count = target_product.stock_count - 1
            target_product.save()
            
            let new_order = Order.create(
                user_id: req.body.user_id,
                total_amount: target_product.price
            )
            respond({"status": "success", "order_id": new_order.id})
        end
    end
end

# 4. Entry Point
action main
    init_db()
    serve(8080)
end

run main`}</code>
            </pre>
          </div>
        </div>

        <Link href="/" className="text-blue-400 hover:underline flex items-center text-lg font-medium">
          <ArrowRight className="w-5 h-5 mr-2 rotate-180" /> Back to Home
        </Link>
      </div>
    </main>
  );
}
